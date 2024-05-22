import os
from dotenv import load_dotenv

load_dotenv()

FRUITSHOP_BASE_URL = os.getenv("FRUITSHOP_BASE_URL", "https://api.predic8.de/shop/v2")

MONGO_URI = os.getenv("MONGO_URI", "")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "app/database/product_hierarchy.db")

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

log_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "%(message)s"
        },
        "detailed": {
            "format": "%(asctime)s %(levelname)s (%(filename)s:%(lineno)d) %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/app.log",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "sync_logger": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"]
    }
}
