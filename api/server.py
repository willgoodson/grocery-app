from fastapi import FastAPI
from pymongo import MongoClient

client = MongoClient(
                    'mongo',
                    username='root',
                    password='example',
                    port=27017
                    )
db = client['grocery-demo']

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get('/api/products/{sku}')
async def products(sku):
    collection = db['products']
    return collection.find_one({'SKU': int(sku)}, {'_id': False})