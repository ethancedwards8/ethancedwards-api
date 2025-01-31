#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse

from jobspy import scrape_jobs

import json, csv

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
        # Create a CSV reader
        csv_reader = csv.DictReader(csv_file)
        # Create a list to store the JSON objects
        json_data = []
        # Iterate over the CSV rows
        for row in csv_reader:
            # Append each row (as a dictionary) to the list
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

class RefreshJobs(Resource):
    def get(self):
        jobs = scrapeJobs()
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(jobs, file, indent=4)
        return f"jobs scraped: {len(jobs)}", 200
