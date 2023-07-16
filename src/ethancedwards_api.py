#!/usr/bin/env python3


# Flask imports
from flask import Flask
from flask_restful import Api, Resource, reqparse

# vanilla imports
import os

# imports for different modules
from quotes.quotes import *

app = Flask(__name__)
api = Api(app)
DEV = os.environ.get('DEV')

# resources being added
api.add_resource(Quote, "/quotes/v1", "/quotes/v1/", "/quotes/v1/<int:id>/")
api.add_resource(Dump, "/quotes/v1/dump", "/quotes/v1/dump/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=(8000 if DEV else 80))
