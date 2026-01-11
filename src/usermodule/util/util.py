from src.usermodule.model.tokenmodel import PromptTokenData
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
from src.config.config import get_req_config

import os
load_dotenv()

def create_prompt_token_data(user_id: str):
    token_data = PromptTokenData(
        user_id=user_id,
        created_at=datetime.now().isoformat(),
        last_updated_at=datetime.now().isoformat(),
        tokens_used=0,
        tokens_balance=2000000,
        total_tokens_used=0
    )

    return token_data.model_dump()


def generate_JWT_token(user_id: str,expriry_time:timedelta):
    JWT_SECRET = get_req_config("JWT_SECRET_KEY")
    ALGORITHM = get_req_config("JWT_ALGORITHM")

    expire = datetime.now(timezone.utc) + expriry_time
    to_encode = {"user_id": user_id}
    to_encode.update({"exp": expire})   
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt