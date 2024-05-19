from pymongo import MongoClient
from app.config import MONGO_URI

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["fruit_store"]
mongo_collection = mongo_db["products"]


# Create necessary indexes for the MongoDB collections.
def create_indexes():
    mongo_collection.create_index("product_id", unique=True, background=True)
    mongo_collection.create_index("children", background=True)
    mongo_collection.create_index("parents", background=True)


def count_products_with_children():
    return mongo_collection.count_documents({"children": {"$exists": True, "$ne": []}})


def find_products_without_parents():
    return mongo_collection.find({"parents": []}, {"_id": False})


def get_docs():
    return mongo_collection.find()


def update_product_by_id(product_id: int, data: dict):
    mongo_collection.update_one({"product_id": product_id}, {"$set": data})
