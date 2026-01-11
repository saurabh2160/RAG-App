from pydantic import BaseModel


class PromptTokenData(BaseModel):
    user_id: str
    created_at: str
    last_updated_at: str
    tokens_used: int
    tokens_balance:int
    total_tokens_used: int