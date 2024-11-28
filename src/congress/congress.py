#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse

import requests
import json
import os

from geocodio import GeocodioClient

# hiding api keys
GEO_KEY = os.environ['GEO_KEY']
CONGRESS_KEY = os.environ['CONGRESS_KEY']

# setup requests for api.congress.gov
CONGRESS_API = "https://api.congress.gov/v3"
congress = requests.Session()
congress.params = { "format": "json" }
congress.headers.update({ "x-api-key": CONGRESS_KEY })

# setup requests for geocodio
client = GeocodioClient(GEO_KEY)

# make json -> dict work. Is there a better way?
true = True
null = None

class RepInfo:
    # nice to have
    def toJSON(self):
        return self.__dict__

    # init class
    def __init__(self, name, ocd_id, reps):
        self.name = name
        self.ocd_id = ocd_id
        self.house = reps[0]

        # for DC, PR, territories, etc, who don't have senators
        if len(reps) > 1:
            self.senate1 = reps[1]
            self.senate2 = reps[2]

        self.__addExtra(reps)

    # add picture and term information from congress API
    def __addExtra(self, reps):
        # storing the object to reduce the amount of requests needed
        self.__houseInfo = self.__getMemberInfo(self.house['references']['bioguide_id'])

        # add pictures and terms of each member
        self.house['picture'] = self.__houseInfo['depiction']['imageUrl']
        self.house['bio']['full_name'] = self.__houseInfo['directOrderName']
        self.house['state'] = self.__houseInfo['state']
        self.house['terms'] = self.__houseInfo['terms']

        # for DC, PR, territories, etc, who don't have senators
        if len(reps) > 1:
            self.__senate1Info = self.__getMemberInfo(self.senate1['references']['bioguide_id'])
            self.__senate2Info = self.__getMemberInfo(self.senate2['references']['bioguide_id'])

            # add pictures and terms of each member
            self.senate1['picture'] = self.__senate1Info['depiction']['imageUrl']
            self.senate1['bio']['full_name'] = self.__senate1Info['directOrderName']
            self.house['state'] = self.__senate1Info['state']
            self.senate1['terms'] = self.__senate1Info['terms']

            self.senate2['picture'] = self.__senate2Info['depiction']['imageUrl']
            self.senate2['bio']['full_name'] = self.__senate2Info['directOrderName']
            self.house['state'] = self.__senate2Info['state']
            self.senate2['terms'] = self.__senate2Info['terms']

            # clean up memory and reduce object json output
            del self.__senate1Info, self.__senate2Info

        # clean up memory and reduce object json output
        del self.__houseInfo

    # pull info from congress API
    def __getMemberInfo(self, bioguideId):
        # eval casts the JSON to a dict
        # get extra information from api.congress.gov. Not super helpful now, but will use this API
        #   to get bill information
        return eval(congress.get(CONGRESS_API + '/member/' + bioguideId).content)['member']

# add api endpoint
class Congress(Resource):
    def get(self, address=None):
        # error handling if a bad address is inputted
        try:
            # roundabout way of mangling the geocodio api to give me the congressional districts!
            congressObject = client.geocode(address, fields=['cd'])['results'][0]['fields']['congressional_districts'][0]

            return RepInfo(congressObject['name'], congressObject['ocd_id'], congressObject['current_legislators']).toJSON(), 200

        except:
            return "address not valid", 404
