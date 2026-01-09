from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from usermodule.controller.usercontroller import add_user


userrouter = APIRouter()

@userrouter.get('/health')
async def health():
    return JSONResponse(content={"status": "ok"})

@userrouter.post('/adduser')
async def add_new_user(request: Request):
    return await add_user(request)
