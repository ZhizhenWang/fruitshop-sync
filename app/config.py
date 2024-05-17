import os
from dotenv import load_dotenv

load_dotenv()

FRUITSHOP_BASE_URL = os.getenv("FRUITSHOP_BASE_URL", "https://api.predic8.de/shop/v2")

MONGO_URI = os.getenv("MONGO_URI", "")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "app/database/product_hierarchy.db")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
