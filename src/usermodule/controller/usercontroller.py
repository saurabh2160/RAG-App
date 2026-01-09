from usermodule.model.model import UserSchema, UserLoginSchema
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse

async def add_user(request: UserSchema):
    try:
        user_collection = request.app.state.services["ragdb"]["users_collection"]
        if not user_collection:
            raise HTTPException(status_code=500, detail="User collection not initialized")
        
        user_data = request.model_dump()
        result = await user_collection.insert_one(user_data)
        if not result:
            raise HTTPException(status_code=500, detail="User creation failed")
        return JSONResponse(content={"message": "User created successfully"}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))