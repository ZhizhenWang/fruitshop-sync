## Step 1: Define environment and dependencies

I use Python v3.11.9, however no latest feature from 3.11 is used in this project. You can also try 3.7 above, but no compatibility guarantee. Also please create clean virtual environment using e.g. pyenv virtualenv or venv

Create one MongoDB database or use the default database in this project.

Install python packages via `pip install -r requirements.txt`, or install manually
  - request package (requests 2.31.0)
  - MongoDB client package (pymongo 4.7.2)
  - OpenAI REST API package (openai 1.30.1)
## Step 2. Manually generate product relation
Simply run following command will generate product relation in SQLite database. The example we use is `12-> 13-> 14`, i.e. product 12 is the parent of product 13, product 13 is the parent of product 14.
```shell
python initialize_relation.py
```


## Step 3. Get data from REST API
To execute step 3-5, please run following command: 
```shell
python main.py
```

Based on fruit shop swagger file `https://api.predic8.de/shop/v2/swagger-ui/index.html` let's first see the response example:

#### Product list response
```json
{
  "meta": {
    "count": 22,
    "start": 11,
    "limit": 10,
    "previous_link": "/shop/v2/products/?start=1&limit=10",
    "next_link": "/shop/v2/products/?start=21&limit=10"
  },
  "products": [
    {
      "id": 1,
      "name": "Banana",
      "self_link": "/shop/v2/products/1"
    }
  ]
}
```
#### Each product detail response
```json
{
  "id": 8,
  "name": "Mangos,",
  "price": 2.79
}
```
#### Vendor list response
```json
{
  "meta": {
    "count": 22,
    "start": 11,
    "limit": 10,
    "previous_link": "/shop/v2/vendors/?start=1&limit=10",
    "next_link": "/shop/v2/vendors/?start=21&limit=10"
  },
  "vendors": [
    {
      "id": 42,
      "name": "Exotic Fruits LLC",
      "self_link": "/shop/v2/vendors/42"
    }
  ]
}
```
#### Each vendor's products response
```json
{
  "meta": {
    "count": 22,
    "start": 11,
    "limit": 10,
    "previous_link": "/shop/v2/products/?start=1&limit=10",
    "next_link": "/shop/v2/products/?start=21&limit=10"
  },
  "products": [
    {
      "id": 1,
      "name": "Banana",
      "self_link": "/shop/v2/products/1"
    }
  ]
}
```

Function `get_products` will get list of products, then for each product it will get its details

Function `get_product_vendors` will first get all vendors (because we cannot get vendor from product endpoint), and for each product the vendor provide, save and return the reversed product-vendor mapping `product_vendors`

## Step 4. Merge and persist data into MongoDB
Function `run` is the main sync function, it merges data from relational database and REST API and consolidates into one MongoDB collection.
Based on the unique id of product, the upsert operation will first insert all new data into collection, and next times only update related document if filter matches corresponding documents.

## Step 5. Run MongoDB query
Function `query` is the required MongoDB query, which includes:
- Number of products with children
- List of products without parents

## Step 6. Get product color through GenAI (Bonus)
Just run following command, it will get color attribute from chatgpt and write into MongoDB
```shell
python chatgpt.py
```

## Final result
Preview of MongoDB products collection
![](imgs\mongodb_schema.png)

Run query result:
```shell
> python main.py

Number of products with children: 2
Products without parents:
{'product_id': 12, 'children': [13], 'name': 'Rambutan', 'parents': [], 'price': 5.6, 'vendors': [{'vendor_id': 1, 'vendor_name': 'Exotics Fruit Lair Ltd.'}], 'color': 'Red'}
{'product_id': 19, 'children': [], 'name': 'Döner', 'parents': [], 'price': 4.5, 'vendors': [], 'color': 'Unknown'}
{'product_id': 20, 'children': [], 'name': 'Figs', 'parents': [], 'price': 2.7, 'vendors': [], 'color': 'Purple'}
{'product_id': 21, 'children': [], 'name': 'Figs', 'parents': [], 'price': 2.7, 'vendors': [], 'color': 'Purple'}
{'product_id': 22, 'children': [], 'name': 'Figs', 'parents': [], 'price': 2.7, 'vendors': [], 'color': 'Purple'}
{'product_id': 23, 'children': [], 'name': 'Mango', 'parents': [], 'price': 2.79, 'vendors': [{'vendor_id': 3, 'vendor_name': 'True Fruits Inc.'}, {'vendor_id': 2, 'vendor_name': 'Max Obsthof GmbH'}], 'color': 'Yellow'}


Process finished with exit code 0
```

Run color generation
```shell
> python chatgpt.py
Rambutan Red
Papaya Orange
Persimmon Orange
Döner Unknown
Figs Purple
Figs Purple
Figs Purple
Mango Yellow


Process finished with exit code 0
```