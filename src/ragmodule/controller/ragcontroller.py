from src.ragmodule.dataloader.data_loader import load_pdf
from src.ragmodule.vectorstore.vectorstrore import VectorStore
from src.ragmodule.reteriver.search import RAGretriever
from fastapi import HTTPException
from fastapi.responses import JSONResponse


async def reterive_user_query(request,user_query,userData):
    try:
        retriever = request.app.state.services["retriever"]
        if not retriever:
            raise HTTPException(status_code=500, detail="RAG retriever not initialized")
 
        query = user_query.get("query")

        if not query:
            return JSONResponse(content={"error": "Query is required","status_code":400})
        
        response = retriever.generate_response(query)
        if not response:
            return  JSONResponse(content={"error": "No response generated","status_code":500})

        return JSONResponse(content={"response": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def add_new_data(file,request):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No selected file")

        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDFs allowed")

        all_docs = await load_pdf(file)
        if not all_docs:
            raise HTTPException(status_code=500, detail="File uploaded failed")
        
        vector_store = VectorStore()
        vectorResponse=vector_store.add_documents(all_docs)

        if not vectorResponse:
            raise HTTPException(status_code=500, detail="File uploaded failed")
        
        request.app.state.services["retriever"] = RAGretriever()
        return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_collection():
    try:
        vector_store = VectorStore()
        result = vector_store.delete_collection()
        if not result:
            raise HTTPException(status_code=500, detail="Collection deletion failed")

        return JSONResponse(content={"message": "Collection deleted successfully"}, status_code=200)
    except Exception as e: # This should be HTTPException
        raise HTTPException(status_code=500, detail=str(e))