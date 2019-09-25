from chalice import Chalice

from pymongo import MongoClient
client = MongoClient("mongodb+srv://Timothy:plati442@cluster0-db0z1.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('Product')
records = db.product_db

from elasticsearch import Elasticsearch
es = Elasticsearch(HOST="http://localhost", PORT=8000)
es = Elasticsearch()

import json

from bson.objectid import ObjectId       # necessary for getting the _id field of each data product from mongoDB

app = Chalice(app_name='Product_App')

# *********
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

"""
A simple CRUD serverless application for Products
"""

# Index function
@app.route('/')
def index():
    return {'hello': 'Welcome to Product Shop'}

# Create a product function
@app.route('/create', methods=['POST'])
def create():
    request = app.current_request                               # this attribute is used to introspect the current HTTP request and save inside the request var
    product = request.json_body                                 # get the json object passed by client and save it inside the product var
    records.insert_one(product)                                 # mongoDB syntax for inseting a document i.e product, into the collection i.e DB table
    return {'feedback': 'Product Created Successfully'}

# Read All products function
@app.route('/read', methods=['GET'])
def readAll():
    return JSONEncoder().encode(list(records.find()))

# Read one product function
@app.route('/{product_id}')
def readOne(product_id):
    key = dict(_id=ObjectId(product_id))                        # the ObjectId function creates a new unique identifier with the product_id suppplied and then
                                                                # a key-value pair is created with it, with _id as key, and then save it inside the key var
    product = records.find_one(key)                             # mongoDB syntax for finding a document
    return JSONEncoder().encode(product)

# Update a product function
@app.route('/{product_id}/update', methods=['PUT'])
def update(product_id):
    request = app.current_request
    key = dict(_id=ObjectId(product_id))
    old_product = records.find_one(key)
    new_product = request.json_body
    new_product = {'$set': new_product}
    records.update_one(old_product, new_product)
    return {'feedback': 'Product Updated Successfully'}

# Delete a product function
@app.route('/{product_id}/delete', methods=['DELETE'])
def delete(product_id):
    key = dict(_id=ObjectId(product_id))
    product = records.find_one(key)
    if product is not None:
        records.delete_one(product)
        return {'feedback': 'Product Deleted Successfully'}
    else:
        return {'feedback': 'Product not Found'}
