#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse

from jobspy import scrape_jobs

import json, csv, os, sys
import base64

currentDir = os.path.dirname(sys.argv[0]) + '/static'

post = reqparse.RequestParser()
post.add_argument('job_url', required=False, type=str, location='args')
post.add_argument('title', required=True, type=str, location='args')
post.add_argument('company', required=True, type=str, location='args')
post.add_argument('location', required=True, type=str, location='args')
post.add_argument('date_posted', required=True, type=str, location='args')
post.add_argument('description', required=True, type=str, location='args')

delete = reqparse.RequestParser()
delete.add_argument('id', required=True, type=str, location='args')

def scrapeJobs():
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "glassdoor"],
        # search_term=jobtype,
        location="Hillsville, VA",
        results_wanted=10,
        hours_old=72,
        country_indeed='USA',
    )

    jobs.to_csv(currentDir + "/jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel

    # is there an easier way to go straight to json?
    with open(currentDir + '/jobs.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = []
        for row in csv_reader:
            json_data.append(row)
    
    # return the formatted json
    return json_data

class JobsList(Resource):
    def get(self, jobtype=None):
        try:
            with open(currentDir + '/data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            return [ ]

    def post(self):
        args = post.parse_args()

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
        if os.path.exists(currentDir + '/data.json'):
            with open(currentDir + '/data.json', 'r', encoding='utf-8') as file:
                tmp = json.load(file)
                # append the new jobs to the existing ones
                tmp.append(job)
        else:
            tmp = job

        with open(currentDir + '/data.json', 'w', encoding='utf-8') as file:
            json.dump(tmp, file, indent=4)

        return job

    def delete(self):
        args = delete.parse_args()

        ret = 0

        id = args['id']

        # pull data out of file
        if os.path.exists(currentDir + '/data.json'):
            with open(currentDir + '/data.json', 'r', encoding='utf-8') as file:
                jobs = json.load(file)

        print(len(jobs))
        for i in range(len(jobs)):
            # find the id request in my list
            if jobs[i]['id'] == id:
                print(f"{i} is {id} in {jobs[i]['title']}")
                ret = jobs[i]
                del jobs[i]
                # so that we only delete the first element that we find. Maybe should be last?
                break

        # put data into file
        with open(currentDir + '/data.json', 'w', encoding='utf-8') as file:
            json.dump(jobs, file, indent=4)

        if ret:
            return ret, 200
        else:
            return "sorry, id not found", 404


class RefreshJobs(Resource):
    def get(self):
        jobs = scrapeJobs()

        tmp = []
        if os.path.exists(currentDir + '/data.json'):
            with open(currentDir + '/data.json', 'r', encoding='utf-8') as file:
                tmp = json.load(file)
                # append the new jobs to the existing ones
                tmp += jobs
        else:
            tmp = jobs

        with open(currentDir + '/data.json', 'w', encoding='utf-8') as file:
            json.dump(tmp, file, indent=4)
        return f"jobs scraped: {len(jobs)}. Total {len(tmp)}", 200

# class HardReset TODO: beware will remove it all maybe PURGE would be better?
