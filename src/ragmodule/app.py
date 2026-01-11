from src.auth.auth import verify_api_key,authenticate_user
from fastapi import APIRouter, Request, UploadFile, Depends
from fastapi.responses import JSONResponse
from src.ragmodule.controller.model import Query
from src.ragmodule.controller.ragcontroller import reterive_user_query,add_new_data,delete_collection


ragrouter = APIRouter()

@ragrouter.get('/health')
async def health():
    return JSONResponse(content={"status": "ok"})

@ragrouter.post('/query')
async def query_rag(user_query: Query, request: Request, auth=Depends(authenticate_user)):
    return await reterive_user_query(request,user_query.model_dump(),auth)


@ragrouter.post('/uploadPdf', dependencies = [Depends(verify_api_key)])
async def add_data(file: UploadFile, request: Request):
    return await add_new_data(file,request)
   

@ragrouter.delete('/deleteCollection',dependencies = [Depends(verify_api_key)])
async def remove_collection(): # require_api_key needs to be adapted as a FastAPI dependency
    return await delete_collection()
   
