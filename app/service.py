from pymongo import UpdateOne

from app.database.mongo import mongo_collection, count_products_with_children, find_products_without_parents, \
    create_indexes, update_product_by_id, get_docs
from app.database.sqlite import get_relation
from app.fruitshop_api import get_products, get_product_vendors
from app.chatgpt import get_color_via_gpt


def run():
    create_indexes()
    # Prepare data to be upsert
    products_data = get_products()
    product_vendors = get_product_vendors()
    relations = get_relation()

    # Merge data and upsert into MongoDB
    requests_list = []

    for product in products_data:
        product_id = product["id"]
        product_name = product["name"]
        product_price = product.get("price", None)

        children = [rel[1] for rel in relations if rel[0] == product_id]
        parents = [rel[0] for rel in relations if rel[1] == product_id]

        product_data = {
            "product_id": product_id,
            "name": product_name,
            "price": product_price,
            "children": children,
            "parents": parents,
            "vendors": product_vendors.get(product_id, [])
        }
        requests_list.append(UpdateOne({"product_id": product_id}, {"$set": product_data}, upsert=True))
    print(requests_list)
    result = mongo_collection.bulk_write(requests_list)
    print(result)


def query():
    # count products with children
    product_with_children_count = count_products_with_children()
    print(f"Number of products with children: {product_with_children_count}")

    # Query to find products without parents
    products_without_parents = find_products_without_parents()
    print("Products without parents:")
    for product in products_without_parents:
        print(product)


# update MongoDB all products' color getting from chatgpt
def update_product_color():
    docs = get_docs()
    for doc in docs:
        product_id = doc.get('product_id')
        product_name = doc.get('name')
        if product_name:
            color = get_color_via_gpt(product_name)
            update_product_by_id(product_id, {"color": color})
            print(product_name, color)
