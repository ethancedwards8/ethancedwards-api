#!/usr/bin/env python3

# Flask imports
from flask import Flask
from flask_restful import Api, Resource, reqparse

# vanilla imports
import os

# imports for different modules
from ethancedwards_api.quotes.quotes import *
from ethancedwards_api.podcast.podcast import *
from ethancedwards_api.congress.congress import *
from ethancedwards_api.audiofeed.audiofeed import *

def main():
    app = Flask(__name__, static_url_path='/static')
    api = Api(app)
    DEV = os.environ.get('DEV')
    
    # deal with CORS crap
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response
    
    # quote resources being added
    api.add_resource(Quote, "/quotes/v1", "/quotes/v1/", "/quotes/v1/<int:id>", "/quotes/v1/<int:id>/")
    api.add_resource(Dump, "/quotes/v1/dump", "/quotes/v1/dump/")
    
    # podcast resources
    api.add_resource(Podcast, "/podcast/v1", "/podcast/v1/", "/podcast/v1/", "/podcast/v1/<int:id>", "/podcast/v1/<int:id>/")
    api.add_resource(PodcastDump, "/podcast/v1/dump", "/podcast/v1/dump/")
    
    api.add_resource(AddressCongress, "/congress/v1/address/<string:address>", "/congress/v1/address/<string:address>/")
    api.add_resource(MemberFetch, "/congress/v1/member/<string:bioguide>", "/congress/v1/member/<string:bioguide>/")
    
    api.add_resource(AudioFeed, "/audiofeed/v1")
    
    app.run(host='0.0.0.0', port=(8000 if DEV else 80))

if __name__ == '__main__':
    main()
