#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse

import requests
import json
import os

# hiding api keys
GITHUB_KEY = os.environ['GITHUB_KEY']

GITHUB_API = "https://api.github.com"
github = requests.Session()
github.params = { "format": "json" }
github.headers.update({ "Authorization": f"Bearer {GITHUB_KEY}" })

parser = reqparse.RequestParser()
parser.add_argument('pr_num', required=True, type=str, location='args')
parser.add_argument('approve', required=False, type=str, location='args', default=False)

class WorkflowRun(Resource):
    def post(self):
        args = parser.parse_args()

        pr_num = args['pr_num']
        approve = args['approve']

        req = github.post(GITHUB_API + '/repos/ethancedwards8/nixpkgs-review-gha/actions/workflows/review.yml/dispatches',
                          json={'ref': 'main', 'inputs': {'pr': str(pr_num), 'approve-on-success': approve }})

        return f"success for {pr_num}", 200
