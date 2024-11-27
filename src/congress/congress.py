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

# make json -> dict work
true = True
null = None

class RepInfo:
    # nice to have
    def toJSON(self):
        return self.__dict__

    def __init__(self, district, reps):
        self.district = district
        self.house = reps[0]
        self.senate1 = reps[1]
        self.senate2 = reps[2]
        self.__addExtra()

    def __addExtra(self):
        # storing the object to reduce the amount of requests needed
        self.__houseInfo = self.__getMemberInfo(self.house['references']['bioguide_id'])
        self.__senate1Info = self.__getMemberInfo(self.senate1['references']['bioguide_id'])
        self.__senate2Info = self.__getMemberInfo(self.senate2['references']['bioguide_id'])

        # add pictures and terms of each member
        self.house['picture'] = self.__houseInfo['depiction']['imageUrl']
        self.house['terms'] = self.__houseInfo['terms']

        self.senate1['picture'] = self.__senate1Info['depiction']['imageUrl']
        self.senate1['terms'] = self.__senate1Info['terms']

        self.senate2['picture'] = self.__senate2Info['depiction']['imageUrl']
        self.senate2['terms'] = self.__senate2Info['terms']

        # clean up memory and reduce object json output
        del self.__houseInfo, self.__senate1Info, self.__senate2Info

    def __getMemberInfo(self, bioguideId):
        # eval casts the JSON to a dict
        return eval(congress.get(CONGRESS_API + '/member/' + bioguideId).content)['member']

class Congress(Resource):
    def get(self, address=None):
        # error handling if a bad address is inputted
        try:
            # roundabout way of mangling the geocodio api to give me the congressional districts!
            congressObject = client.geocode(address, fields=['cd'])['results'][0]['fields']['congressional_districts'][0]

            return RepInfo(congressObject['ocd_id'], congressObject['current_legislators']).toJSON(), 200

        except:
            return "address not vald", 404
