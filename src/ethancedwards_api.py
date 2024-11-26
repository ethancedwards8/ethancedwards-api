#!/usr/bin/env python3


# Flask imports
from flask import Flask
from flask_restful import Api, Resource, reqparse

# vanilla imports
import os

# imports for different modules
from quotes.quotes import *
from podcast.podcast import *
from congress.congress import *

app = Flask(__name__)
api = Api(app)
DEV = os.environ.get('DEV')

# quote resources being added
api.add_resource(Quote, "/quotes/v1", "/quotes/v1/", "/quotes/v1/<int:id>", "/quotes/v1/<int:id>/")
api.add_resource(Dump, "/quotes/v1/dump", "/quotes/v1/dump/")

# podcast resources
api.add_resource(Podcast, "/podcast/v1", "/podcast/v1/", "/podcast/v1/", "/podcast/v1/<int:id>", "/podcast/v1/<int:id>/")
api.add_resource(PodcastDump, "/podcast/v1/dump", "/podcast/v1/dump/")

api.add_resource(Congress, "/congress/v1/<string:address>", "/congress/v1/<string:address>/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=(8000 if DEV else 80))
