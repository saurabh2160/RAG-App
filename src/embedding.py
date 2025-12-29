import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
logging.basicConfig(level=logging.INFO)



class EmbeddingPipeline:
    def __init__(self,model_name:str = "all-MiniLM-L6-v2",chunk_size:int = 1000,chunk_overlap:int=200):
        #initialize embedding manger
        #args : huggingFace modal name for sentence embeddings
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        try:
            self.model = SentenceTransformer(model_name)
            logging.info(f'Model loaded success .Embedding dimension :{self.model.get_sentence_embedding_dimension()}')
        except Exception as e:
            logging.info(f"error loading model {model_name}:{e}")
            raise

    def chunk_documents(self,documents:List[Any]) -> List[Any]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ",""]
        )
        chunks = splitter.split_documents(documents)
        logging.info(f'Split {len(documents)} documents into {len(chunks)} chunks')
        return chunks

    # def embed_documents(self, documents: List[Any]) -> np.ndarray:
    #     chunks = self.chunk_documents(documents)
    #     embeddings= self.model.encode( [chunk.page_content for chunk in chunks],show_progress_bar=True)
    #     logging.info(f'genrated embeddings of {len(embeddings)} chunks')
    #     return embeddings
    
    def embed_chunks(self,chunks:List[Any]) -> np.ndarray:
        texts = [chunk.page_content for chunk in chunks]
        logging.info(f'generating embeding for {len(texts)} texts..')
        embeddings= self.model.encode(texts,show_progress_bar=True)
        logging.info(f'genrated embedding with shape {embeddings.shape}')
        return embeddings
    
    def generate_embeddings(self, texts: List[Any]) -> np.ndarray:
        #genrate embeddings for list of texts
        # arg : texts  list of text strings to embed 
        # return : numpy array of embeddings with shape (len(texts) ,embeding_dimensin)

        if not self.model:
            raise ValueError('model not loaded')
        logging.info(f'generating embeding for {len(texts)} texts..')
        embeddings= self.model.encode(texts,show_progress_bar=True)
        logging.info(f'genrated embedding with shape {embeddings.shape}')
        return embeddings


