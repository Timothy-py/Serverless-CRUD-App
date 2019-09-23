from chalice import Chalice

from pymongo import MongoClient
client = MongoClient("mongodb+srv://Timothy:plati442@cluster0-db0z1.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('Product')
records = db.product_db

from elasticsearch import Elasticsearch
es = Elasticsearch(HOST="http://localhost", PORT=8000)
es = Elasticsearch()

import json
from bson import ObjectId

app = Chalice(app_name='Product_App')


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
    return {'message': 'Product Created Successfully'}

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
    product = table.find_one({'name': name})
    body = request.json_body
    new_product = {'$set': body}
    records.update_one(data, new_data)
    return {'message': 'Product Updated Successfully'}

@app.route('/{name}/delete', methods=['POST'])
def delete(name):
    product = records.find_one({'name': name})
    if product is not None:
        records.delete_one(product)
        return {'message': 'Product Deleted Successfully'}
    else:
        return {'message': 'Product not Found'}






# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
