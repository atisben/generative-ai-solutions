from loguru import logger
from pathlib import Path
import os
import sys
from dotenv import load_dotenv
load_dotenv(override=True)

class Config:
    SEED=42
    ALLOWED_FILE_EXTENSIONS = set([".pdf", ".md", ".txt"])

    class Model:
        NAME = "deepseek-r1:7b"
        TEMPERATURE = 0.6


    class Preprocessing:
        CHUNK_SIZE = 2048
        CHUNK_OVERLAP = 128
        EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
        RERANKER = "ms-marco-MiniLM-L-12-v2"
        LLM = "llama3.2"
        CONTEXTUALIZE_CHUNKS = True
        N_SEMANTIC_RESULTS = 5
        N_BM25_RESULTS = 5

    class Chatbot:
        N_CONTEXT_RESULTS = 3

    class Path:
        APP_HOME = Path(Path(__file__).parent.parent, os.getenv("APP_HOME"))
        DATA_DIR = APP_HOME/"data"
        DB_DIR = DATA_DIR/"chroma_langchain_db"
    
    class VectorStore:
        COLLECTION_NAME = "example_collection"


def configure_logging():  
    config = {  
        "handlers": [  
            {  
                "sink": sys.stdout,  
                "colorize": True,  
                "format": "<green>{time}</green> <level>{message}</level>",  
            }  
        ]  
    }  
    # Remove any previously installed handlers  
    logger.remove()  
    # Configure loguru logger based on the provided configuration  
    logger.configure(**config)  
  
    # Optionally, you can add more customization or set log level  
    logger.info("Logging is configured.")  
    return logger
  