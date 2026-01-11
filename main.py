from src.ragmodule.reteriver.search import RAGretriever
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from src.config.config import get_req_config
import os
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")



@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting services...")
    logging.info("Connecting to MongoDB...")
    mongo_uri = get_req_config("MONGO_URL")
    client = AsyncIOMotorClient(mongo_uri)
    if not client:
        logging.info("MongoDB connection failed")
    logging.info("Connected to MongoDB")
    retriever = RAGretriever()
    app.state.services = {
        "retriever":retriever,
        "mongo_client": client
    }
    yield
    logging.info("Shutting down services...")
    logging.info("Disconnecting from MongoDB...")
    await client.close()
    logging.info("Disconnected from MongoDB")
    logging.info("✅ Services stopped")

app = FastAPI(lifespan=lifespan)
from src.ragmodule.app import ragrouter
from src.usermodule.index import userrouter

app.include_router(ragrouter,prefix='/rag/v1')
app.include_router(userrouter,prefix='/user/v1')

