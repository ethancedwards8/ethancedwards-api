#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse

from jobspy import scrape_jobs

import json, csv, os
import base64

parser = reqparse.RequestParser()
parser.add_argument('job_url', required=False, type=str, location='args')
parser.add_argument('title', required=True, type=str, location='args')
parser.add_argument('company', required=True, type=str, location='args')
parser.add_argument('location', required=True, type=str, location='args')
parser.add_argument('date_posted', required=True, type=str, location='args')
parser.add_argument('description', required=True, type=str, location='args')

jobs = [ ]

def scrapeJobs():
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
        # search_term=jobtype,
        location="Hillsville, VA",
        results_wanted=10,
        hours_old=72,
        country_indeed='USA',
    )

    jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel

    # is there an easier way to go straight to json?
    with open('jobs.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = []
        for row in csv_reader:
            json_data.append(row)
    
    # return the formatted json
    return json_data

class JobsList(Resource):
    def get(self, jobtype=None):
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            return [ ]

    def post(self):
        args = parser.parse_args()

        job = {
            'id': f"cm-{str(hash(args['title'] + args['company']))}",
            'job_url': args.get('job_url') or '',
            'title': args['title'],
            'company': args['company'],
            'location': args['location'],
            'date_posted': args['date_posted'],
            'description': args['description']
        }

        tmp = []
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as file:
                tmp = json.load(file)
                # append the new jobs to the existing ones
                tmp.append(job)
        else:
            tmp = job

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(tmp, file, indent=4)

        return job


class RefreshJobs(Resource):
    def get(self):
        jobs = scrapeJobs()

        tmp = []
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as file:
                tmp = json.load(file)
                # append the new jobs to the existing ones
                tmp += jobs
        else:
            tmp = jobs

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(tmp, file, indent=4)
        return f"jobs scraped: {len(jobs)}. Total {len(tmp)}", 200

# class HardReset TODO: beware will remove it all
