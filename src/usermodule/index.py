from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from src.usermodule.controller.usercontroller import add_user_and_create_token_Data, login_user_and_generate_token
from src.usermodule.model.usermodel import UserSchema, UserLoginSchema

userrouter = APIRouter()

@userrouter.get('/health')
async def health():
    return JSONResponse(content={"status": "ok"})

@userrouter.post('/adduser')
async def add_new_user(user_data: UserSchema,request: Request):
    return await add_user_and_create_token_Data(request,user_data.model_dump())

@userrouter.post('/login')
async def login_user(user_login_data: UserLoginSchema, request: Request):
    return await login_user_and_generate_token(request, user_login_data.model_dump())
