from src.reteriver.search import RAGretriever
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from dotenv import load_dotenv
import os
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Starting services...")
    logging.info("Connecting to MongoDB...")
    mongo_uri = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(mongo_uri)
    if not client:
        logging.info("MongoDB connection failed")
    logging.info("Connected to MongoDB")
    retriever = RAGretriever()
    app.state.services = {
        "retriever":retriever,
        "ragdb": client["ragdb"] if client else None
    }
    yield
    logging.info("🛑 Shutting down services...")
    logging.info("Disconnecting from MongoDB...")
    await client.close()
    logging.info("Disconnected from MongoDB")
    logging.info("✅ Services stopped")

app = FastAPI(lifespan=lifespan)
from src.app import ragrouter

app.include_router(ragrouter,prefix='/rag/v1')

