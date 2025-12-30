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
from ethancedwards_api.jobs.jobs import *
from ethancedwards_api.nixpkgs.nixpkgs import *

static_dir = os.path.dirname(sys.argv[0]) + '/static'

def main():
    app = Flask(__name__, static_url_path='/static', static_folder=static_dir)
    api = Api(app)
    DEV = os.environ.get('DEV')
    
    # deal with CORS crap
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
        return response
    
    # quote resources being added
    api.add_resource(Quote, "/quotes/v1", "/quotes/v1/", "/quotes/v1/<int:id>", "/quotes/v1/<int:id>/")
    api.add_resource(Dump, "/quotes/v1/dump", "/quotes/v1/dump/")
    
    # podcast resources
    api.add_resource(Podcast, "/podcast/v1", "/podcast/v1/", "/podcast/v1/", "/podcast/v1/<int:id>", "/podcast/v1/<int:id>/")
    api.add_resource(PodcastDump, "/podcast/v1/dump", "/podcast/v1/dump/")
    
    api.add_resource(AddressCongress, "/congress/v1/address/<string:address>", "/congress/v1/address/<string:address>/")
    api.add_resource(MemberFetch, "/congress/v1/member/<string:bioguide>", "/congress/v1/member/<string:bioguide>/")
    
    api.add_resource(AudioFeed, "/audiofeed/v1", "/audiofeed/v1/", "/audiofeed/v1/dump")

    # jobs
    api.add_resource(JobsList, "/jobs/v1",  "/jobs/v1/")
    api.add_resource(RefreshJobs, "/jobs/v1/refresh",  "/jobs/v1/refresh/")

    api.add_resource(WorkflowRun, "/nixpkgs/v1")
    
    app.run(host='0.0.0.0', port=(8000 if DEV else 80))

if __name__ == '__main__':
    main()
