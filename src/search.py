from src.vectorstrore import VectorStore
from src.embedding import EmbeddingPipeline as EmbeddingManager
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
logging.basicConfig(level=logging.INFO)




class RAGretriever: #this is build on top of vector db its a interface 
    #handles query based retirival from vector store
    def __init__(self):
        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path=env_path,override=True)
        API_KEY = os.getenv("GROK_API_KEY")
        self.vector_store = VectorStore()
        self.embedding_manager = EmbeddingManager()
        ### initialize llm model
        self.llm = ChatGroq(
            groq_api_key=API_KEY,
            temperature=0.1,
            max_tokens=1024,
            model="groq/compound"
        )
        logging.info("RAG retriever initialized")

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0) -> List[Dict[str,Any]]:
        #retrieve releavant docs for a given query
        #args :  query -> search query, top_k -> Nuber of top results to return, score_threshold -> minimum similarity score threshold
        
        logging.info(f'retrieving docs for:{query}')
        logging.info(f'top k {top_k} scr threshold :{score_threshold}')
        
        #genrate query embedding
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]

        #search vector db
        try:
            results = self.vector_store.collection.query( 
                query_embeddings= [query_embedding.tolist()],
                n_results=top_k,
            )
            #process results
            retrieved_docs = []
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]
            
                for i, (doc_id,doc,metadata,distance) in enumerate(zip(ids,documents,metadatas,distances)):
                    
                    similarity_score = 1 - float(distance) #convert distance to similarity score
                    if similarity_score >= score_threshold:
                        retrieved_docs.append({
                            'id':doc_id,
                            'content':doc,
                            'metadata':metadata,
                            'similarity_score':similarity_score,
                            'rank':i+1
                        })
                
                logging.info(f'Retrieved {len(retrieved_docs)} documents after filtering')
            else:
                logging.info('No documents found')
                
            return retrieved_docs
        except Exception as e:
            logging.info(f'got err from retrieving:{e}')
            return []
    
    def generate_response(self,query:str,top_k=5,min_score=0.2,return_context=False):
        ## extra features returns ans,source,confidence score, and full context
        results = self.retrieve(query,top_k,score_threshold=min_score)
        if not results:
            return {'ans':'no context found','sources':[],'context':'','confidence':0.0}
        
        
        #prepare context and sources
        context = "\n\n".join([doc['content'] for doc in results])
        if not context:
            return "No releavent context was found"
        sources = [{
            'source':doc['metadata'].get('source_file',doc['metadata'].get('source','unknown')),
            'page':doc['metadata'].get('page','unknown'),
            'score':doc['similarity_score'],
            'preview':doc['content'][:300] + '...'
        }for doc in results]
        # confidence = max([doc['similarity_score'] for doc in results])
        confidence = sum(doc['similarity_score'] for doc in results) / len(results)
        #genrate ans
        prompt = f"""
            You are a helpful AI assistant.
            Answer ONLY using the provided context.
            If the answer is not present, say "Not found in context".

            Context:
            {context}

            Question:
            {query}

            Answer (concise):
        """
        response = self.llm.invoke(prompt)
        output = {
            "query": query,
            "answer": response.content.strip(),
            "confidence": round(confidence, 3),
            "sources": sources,
            "context_used": return_context
        }
        if return_context:
            output['context'] = context
            
        return output