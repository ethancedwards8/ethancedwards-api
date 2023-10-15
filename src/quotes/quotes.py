from flask_restful import Api, Resource, reqparse

import random
import os
import json

with open(os.path.dirname(os.path.realpath(__file__)) + '/quotes.json') as f:
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
