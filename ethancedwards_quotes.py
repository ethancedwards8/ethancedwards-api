#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse

import random
import os
import json

app = Flask(__name__)
api = Api(app)

DEV = os.environ.get('DEV')

with open('quotes.json') as f:
    quotes = json.load(f)

class Quote(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(quotes), 200
        quote = quotes[id]

        if quote:
            return quote, 200, {'Access-Control-Allow-Origin': '*'}

        return "quote not found", 404


class Dump(Resource):
    def get(self):
        return quotes, 200


api.add_resource(Quote, "/quotes/v1", "/quotes/v1/", "/quotes/v1/<int:id>/")
api.add_resource(Dump, "/quotes/v1/dump", "/quotes/v1/dump/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=(8000 if DEV else 80))
