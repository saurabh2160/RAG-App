from pydantic import BaseModel


class Query(BaseModel):
    query: str

class RAGResponse(BaseModel):
    query: str
    response: str
