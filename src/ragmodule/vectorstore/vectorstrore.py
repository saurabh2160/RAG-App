import os
import chromadb
from typing import List, Any
import uuid
from src.ragmodule.embed.embedding import EmbeddingPipeline
import logging
logging.basicConfig(level=logging.INFO)

class VectorStore:
    def __init__(self,collection_name:str="documentstore",persist_directory:str="../data/vector_store"):
        os.makedirs(persist_directory,exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "document embedding for RAG pipeline",
                "hnsw:space": "cosine"
            }
        )
        self.emb_pipeline = EmbeddingPipeline()
        logging.info(f'vector db initialized, Collection:{collection_name}')
        logging.info(f'existing documents in colletion: {self.collection.count()}')
        
    def add_documents(self,documents:List[Any]):
        if not documents:
            logging.info("No documents to add")
            return
        chunked_doc = self.emb_pipeline.chunk_documents(documents)
        embeddings = self.emb_pipeline.embed_chunks(chunked_doc)
        if len(chunked_doc) != len(embeddings):
            raise ValueError("Docs len not match embed len")

        #prepare data for chrorma db
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        
        for i,(doc,embedding) in enumerate(zip(chunked_doc,embeddings)):
            # genrate unique id
            doc_id = f"doc_{uuid.uuid4().hex[:12]}"
            ids.append(doc_id)

            #prepare metadata
            metadata = dict(doc.metadata or {})
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadata["hnsw:space"] = "cosine"
            metadatas.append(metadata)

            #doc context
            documents_text.append(doc.page_content)

            #embedding
            embeddings_list.append(embedding.tolist())
        
        #add to collection
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                metadatas=metadatas,
                documents=documents_text
            )
            logging.info(f'Successfully added {len(chunked_doc)} documents to vector store')
            logging.info(f'Total documents in collection: {self.collection.count()}')
            return True
        except Exception as e:
            logging.info(f'err in adding docs to collection:{e}')
            return False
        
    def clear_documents(self):
        try:
            self.collection.delete(where={

            })
            logging.info("All documents deleted from collection")
            logging.info(f"Current count: {self.collection.count()}")
            return True
        except Exception as e:
            logging.info(f"Error clearing documents: {e}")
            return False

    def delete_collection(self):
        try:
            self.client.delete_collection(name=self.collection.name)
            logging.info(f"Collection '{self.collection.name}' deleted")
            return True
        except Exception as e:
            logging.info(f"Error deleting collection: {e}")
            return False
