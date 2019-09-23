from chalice import Chalice

from pymongo import MongoClient
client = MongoClient("mongodb+srv://Timothy:plati442@cluster0-db0z1.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('Product')
records = db.product_db

from elasticsearch import Elasticsearch
es = Elasticsearch(HOST="http://localhost", PORT=8000)
es = Elasticsearch()

import json

from bson import ObjectId       # necessary for getting the _id field of each data product from mongoDB

app = Chalice(app_name='Product_App')

# *********
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/')
def index():
    return {'hello': 'Welcome to Product Shop'}


@app.route('/create', methods=['POST'])
def create():
    request = app.current_request
    body = request.json_body
    records.insert_one(body)
    return {'feedback': 'Product Created Successfully'}

@app.route('/read', methods=['GET'])
def readAll():
    return JSONEncoder().encode(list(records.find()))

@app.route('/{name}')
def readOne(name):
    product = records.find_one({'name': name})
    return JSONEncoder().encode(product)

@app.route('/{name}/update', methods=['POST'])
def update(name):
    request = app.current_request
    product = records.find_one({'name': name})
    body = request.json_body
    new_product = {'$set': body}
    records.update_one(data, new_data)
    return {'feedback': 'Product Updated Successfully'}

@app.route('/{name}/delete', methods=['POST'])
def delete(name):
    product = records.find_one({'name': name})
    if product is not None:
        records.delete_one(product)
        return {'feedback': 'Product Deleted Successfully'}
    else:
        return {'feedback': 'Product not Found'}
