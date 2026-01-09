from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse as jsonify
from dotenv import load_dotenv
import os
load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    # Retrieve the expected API key from the environment variables.
    server_key = os.getenv("SECRET_KEY_API")
    if not server_key:
        raise HTTPException(status_code=500, detail="Server API key not configured")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")
    if api_key != server_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return True
