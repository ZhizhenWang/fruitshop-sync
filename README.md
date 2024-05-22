## Step 1: Define environment and dependencies
### Python environment and packages
For this project I use Python v3.11.9, however no latest feature from 3.11 is used in this project. You can also try 3.7 above, but no compatibility guarantee. Also please create clean virtual environment using e.g. pyenv virtualenv or venv

Install python packages via `pip install -r requirements.txt`, or install manually
  - request package (requests 2.31.0)
  - MongoDB client package (pymongo 4.7.2)
  - OpenAI REST API package (openai 1.30.1)
  - package to load environment variable from .env file (python-dotenv 1.0.1)
### MongoDB setup
Create one MongoDB database and set env variable `MONGO_URI` value.

### Environment variables
Following table lists all environment variables, you can set them in `.env` file or bash

#### .env file exmaple:
```
MY_VARIABLE=value
```
#### Bash example
```bash
export MY_VARIABLE="value"
```

| Environment Variable | Usage                 | Default Value                     |
|:---------------------|:----------------------|:----------------------------------|
| FRUITSHOP_BASE_URL   | Url of fruit shop api | https://api.predic8.de/shop/v2    |
| MONGO_URI            | MongoDB URI           |                                   |
| SQLITE_DB_PATH       | SQLite file location  | app/database/product_hierarchy.db |
| OPENAI_BASE_URL      | OpenAI REST API URL   | https://api.openai.com/v1         |
| OPENAI_API_KEY       | OpenAI REST API Key   |                                   |

Please get ChatGPT API Key from [here](https://platform.openai.com/api-keys) and set corresponding env `OPENAI_API_KEY` value. You can set env `OPENAI_API_BASE` to use alternative gpt proxy.

## Step 2. Manually generate product relation
Simply run following command will generate product relation in SQLite database. The example we use is `12-> 13-> 14`, i.e. product 12 is the parent of product 13, product 13 is the parent of product 14.
```shell
python main.py initdb
```

## Step 3. Synchronize fruit shop API data and relation data into MongoDB
Please run following command to synchronize into MongoDB
```shell
python main.py sync
```

### Fetch data from fruit ship API
Here's the explanation of `app/fruitshop_api.py`. Based on fruit shop swagger file `https://api.predic8.de/shop/v2/swagger-ui/index.html` let's first see the response example:

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

### Merge and persist data into MongoDB
Function `run` is the main sync function, it merges data from relational database and REST API and consolidates into one MongoDB collection.

The `products` collection stores bidirectional(stores both its parents and children) relation to speed up query.

As required upsert MongoDB operation is used, because based on the unique id of product, the upsert operation will first insert all new data into collection, and next times only update related document if filter matches corresponding documents. 

And we use `bulk_write`, which performs batch operations on multiple documents within a collection. It executes efficiently multiple write operations in a single request.

## Step 4. Run MongoDB query

Run following command to execute preset MongoDB query, which includes:
- Number of products with children
- List of products without parents
```shell
> python main.py query

Number of products with children: 2
Products without parents:
{'product_id': 12, 'children': [13], 'name': 'Rambutan', 'parents': [], 'price': 5.6, 'vendors': [{'vendor_id': 1, 'vendor_name': 'Exotics Fruit Lair Ltd.'}], 'color': 'Red'}
{'product_id': 19, 'children': [], 'name': 'Döner', 'parents': [], 'price': 4.5, 'vendors': [], 'color': 'Unknown'}
{'product_id': 20, 'children': [], 'name': 'Figs', 'parents': [], 'price': 2.7, 'vendors': [], 'color': 'Purple'}
{'product_id': 21, 'children': [], 'name': 'Figs', 'parents': [], 'price': 2.7, 'vendors': [], 'color': 'Purple'}
{'product_id': 22, 'children': [], 'name': 'Figs', 'parents': [], 'price': 2.7, 'vendors': [], 'color': 'Purple'}
{'product_id': 23, 'children': [], 'name': 'Mango', 'parents': [], 'price': 2.79, 'vendors': [{'vendor_id': 3, 'vendor_name': 'True Fruits Inc.'}, {'vendor_id': 2, 'vendor_name': 'Max Obsthof GmbH'}], 'color': 'Yellow'}
```

## Step 5. Get product color through GenAI (Bonus)
Just run following command, it will get color attribute from chatgpt and update `products` collection in MongoDB.
```shell
> python main.py update

python main.py update
Rambutan Red
Papaya Orange
Persimmon Orange
Döner Unknown
Figs Purple
Mango Yellow
Banana Yellow
Blackberry Black
Cherry Red
Coconut Brown
Dragon-Fruit Pink
Fig Purple
Gac-Fruit Red
Grapes Purple
...

```

## Final result

Based on platform you can query data via MongoDB Shell

Here use macOS as an example:
```shell
# Connect to mongodb database and enter password
mongosh <your_mongo_uri> --apiVersion 1 --username <your_mongo_user>

# After login, switch to the desired database
use fruit_store

# Get first 10 documents in a collection by running a query
db.products.find().limit(10)
```

Preview of MongoDB products collection

<img src="imgs\mongodb_schema.png" width="80%">


## Feature work

- api query can fetch first 100 items due to limit, need to refactor code to fetch all items
- ~~use logging package instead of print~~
- add create_time and update_time in mongo `products` collection
- ask chatgpt about product color based on product image