import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SILICON_API_KEY = os.getenv("SILICON_API_KEY")
    EMBEDDING_MODEL = "BAAI/bge-m3"
    IMAGE_DIR = os.path.join(os.path.dirname(__file__), '../data/images')
    CACHE_FILE = os.path.join(os.path.dirname(__file__), '../data/embeddings.pkl') 