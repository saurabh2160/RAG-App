from src.usermodule.model.usermodel import UserCreateResponse,UserLoginResponse
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from src.usermodule.util.util import create_prompt_token_data,generate_JWT_token

async def add_user_and_create_token_Data(request,user_data):
    try:
        mongo_client = request.app.state.services["mongo_client"]
        user_collection = mongo_client["RAG-DB"]["users_collection"]
        token_collection = mongo_client["RAG-DB"]["token_usage_collection"]
        async with await mongo_client.start_session() as session:
            async with session.start_transaction():
                # Add extra keys to user_data before inserting
                user_data_dict = user_data
                user_data_dict["created_at"] = datetime.now().isoformat()
                user_data_dict["last_updated_at"] = datetime.now().isoformat()

                # Check if a user with the same email already exists
                existing_user = await user_collection.find_one({"email": str(user_data_dict["email"])})
                if existing_user:
                    await session.abort_transaction()
                    return HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="User with this email already exists"
                    )
                result = await user_collection.insert_one(
                    user_data_dict, 
                    session=session
                )
                if not result.acknowledged:
                    await session.abort_transaction()
                    return HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to create user"
                    )
                # generate access token
                access_token = generate_JWT_token(str(result.inserted_id),30)
                # Create token data
                token_data = create_prompt_token_data(str(result.inserted_id))
                token_result = await token_collection.insert_one(token_data, session=session)

                if not token_result.acknowledged:
                    await session.abort_transaction()
                    return HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to create token data"
                    )
                
                # If both operations succeed, commit the transaction
                await session.commit_transaction()
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=UserCreateResponse(message="New user created successfully", token=access_token).model_dump()
        )
    except Exception as e:
        print(f"User creation error: {str(e)}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def login_user_and_generate_token(request, user_login_data):
    try:
        mongo_client = request.app.state.services["mongo_client"]
        user_collection = mongo_client["RAG-DB"]["users_collection"]
        user = await user_collection.find_one({"email": str(user_login_data['email'])})

        if not user:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not user_login_data["password"] ==  user["password"]:
            return  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

        access_token = generate_JWT_token(str(user["_id"]), timedelta(minutes=30))
        refresh_token = generate_JWT_token(str(user["_id"]),timedelta(minutes=60 * 24 * 7))
        
        # Store refresh token in user collection
        update_result = await user_collection.update_one({"_id": user["_id"]}, {"$set": {"refresh_token": refresh_token}})
        
        if not update_result.acknowledged or update_result.modified_count == 0:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store refresh token"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= UserLoginResponse(
                message="Login successful",
                token=access_token
            ).model_dump()
        )
    except Exception as e:
        print(f"User login error: {str(e)}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
