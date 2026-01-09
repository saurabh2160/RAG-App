from src.dataloader.data_loader import load_pdf
from src.vectorstore.vectorstrore import VectorStore
from src.reteriver.search import RAGretriever
from src.auth.auth import verify_api_key
from fastapi import APIRouter, Request, HTTPException, UploadFile, Depends
from fastapi.responses import JSONResponse


ragrouter = APIRouter()

@ragrouter.get('/health')
async def health():
    return JSONResponse(content={"status": "ok"})

@ragrouter.post('/query')
async def query_rag(request: Request):
    try:
        retriever = request.app.state.services["retriever"]
        if not retriever:
            raise HTTPException(status_code=500, detail="RAG retriever not initialized")
        data = await request.json()
        query = data.get("query")

        if not query:
            return JSONResponse(content={"error": "Query is required","status_code":400})
        
        response = retriever.generate_response(query)
        if not response:
            return  JSONResponse(content={"error": "No response generated","status_code":500})

        return JSONResponse(content={"response": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ragrouter.post('/uploadPdf')
async def add_new_data(file: UploadFile, request: Request, auth=Depends(verify_api_key)):
    try:
        if auth:
            pass
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

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

@ragrouter.get('/deleteCollection')
async def delete_collection(): # require_api_key needs to be adapted as a FastAPI dependency
    try:
        vector_store = VectorStore()
        result = vector_store.delete_collection()
        if not result:
            raise HTTPException(status_code=500, detail="Collection deletion failed")

        return JSONResponse(content={"message": "Collection deleted successfully"}, status_code=200)
    except Exception as e: # This should be HTTPException
        raise HTTPException(status_code=500, detail=str(e))
