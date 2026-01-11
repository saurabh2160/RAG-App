from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from src.config.config import get_req_config
import jwt



def verify_api_key(api_key_in_req_header:str = Depends(APIKeyHeader(name="X-API-Key", auto_error=False))):
    # Retrieve the expected API key from the environment variables.
    server_key = get_req_config("SECRET_KEY_API")
    if not server_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server API key not configured")
    if not api_key_in_req_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key missing")
    if api_key_in_req_header != server_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")


def authenticate_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    try:
        payload = jwt.decode(token, get_req_config("JWT_SECRET_KEY"), algorithms=[get_req_config("JWT_ALGORITHM")])
        if not payload or not payload.get("user_id"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return {"user_id": payload.get("user_id"),"is_authenticated":True}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

