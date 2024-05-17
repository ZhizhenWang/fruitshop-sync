import requests

from app.config import FRUITSHOP_BASE_URL


# Function to get product details by id
def get_product_details(product_id: int) -> dict:
    whitelist_key = ["id", "name", "price"]
    product_url = f"{FRUITSHOP_BASE_URL}/products/{product_id}"
    product_response = requests.get(product_url).json()
    return {key: value for key, value in product_response.items() if key in whitelist_key}


# Function to get products from API
def get_products() -> list:
    # TODO: limit set to 100, if count > 100 need to increase limit or retrieve in loop
    products_url = f"{FRUITSHOP_BASE_URL}/products?limit=100"
    response = requests.get(products_url)
    product_list = response.json()

    products_data = []
    for product in product_list["products"]:
        product_id = product["id"]
        product_details = get_product_details(product_id)
        products_data.append(product_details)
    return products_data


# Function to get product to vendors mapping from API
def get_product_vendors() -> dict:
    # TODO: same limited result here
    vendors_url = f"{FRUITSHOP_BASE_URL}/vendors?limit=100"
    vendors_response = requests.get(vendors_url)
    vendors_data = vendors_response.json()
    product_vendors = {}

    for vendor in vendors_data["vendors"]:
        vendor_id = vendor["id"]
        vendor_name = vendor["name"]
        # TODO: same limited result here
        products_url = f"{FRUITSHOP_BASE_URL}/vendors/{vendor_id}/products?limit=100"
        products_response = requests.get(products_url)
        products_data = products_response.json()

        for product in products_data["products"]:
            product_id = product["id"]
            if product_id not in product_vendors:
                product_vendors[product_id] = []
            product_vendors[product_id].append({"vendor_id": vendor_id, "vendor_name": vendor_name})
    return product_vendors
