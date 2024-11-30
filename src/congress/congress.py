#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse

import requests
import json
import os
from enum import Enum

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

class LegislationTypeEnum(Enum):
    SPONSORED = 1
    COSPONSORED = 2

class RepInfo:
    # nice to have
    def toJSON(self):
        return self.__dict__

    # init class
    def __init__(self, name, ocd_id, reps, address):
        self.name = name
        self.ocd_id = ocd_id
        # needed later for data retrieval
        self.address = address
        self.house = reps[0]

        # for DC, PR, territories, etc, who don't have senators
        if len(reps) > 1:
            self.senate1 = reps[1]
            self.senate2 = reps[2]

        self.__addExtra(reps)

    # add picture and term information from congress API
    def __addExtra(self, reps):
        # storing the object to reduce the amount of requests needed
        self.__houseInfo = RepInfo.getMemberInfo(self.house['references']['bioguide_id'])

        # add pictures and terms of each member
        self.house['type'] = self.house['type'].capitalize()
        self.house['picture'] = self.__houseInfo['depiction']['imageUrl']
        self.house['bio']['full_name'] = self.__houseInfo['directOrderName']
        self.house['state'] = self.__houseInfo['state']
        self.house['sponsoredLegislationCount'] = self.__houseInfo['sponsoredLegislation']['count']
        self.house['cosponsoredLegislationCount'] = self.__houseInfo['cosponsoredLegislation']['count']
        self.house['terms'] = self.__houseInfo['terms']
        self.house['typeSince'] = RepInfo.findYearOfOffice(self.house)

        # for DC, PR, territories, etc, who don't have senators
        if len(reps) > 1:
            self.__senate1Info = RepInfo.getMemberInfo(self.senate1['references']['bioguide_id'])
            self.__senate2Info = RepInfo.getMemberInfo(self.senate2['references']['bioguide_id'])

            # add pictures and terms of each member
            self.senate1['type'] = self.senate1['type'].capitalize()
            self.senate1['picture'] = self.__senate1Info['depiction']['imageUrl']
            self.senate1['bio']['full_name'] = self.__senate1Info['directOrderName']
            self.senate1['state'] = self.__senate1Info['state']
            self.senate1['sponsoredLegislationCount'] = self.__senate1Info['sponsoredLegislation']['count']
            self.senate1['cosponsoredLegislationCount'] = self.__senate1Info['cosponsoredLegislation']['count']
            self.senate1['terms'] = self.__senate1Info['terms']
            self.senate1['typeSince'] = RepInfo.findYearOfOffice(self.senate1)

            self.senate2['type'] = self.senate2['type'].capitalize()
            self.senate2['picture'] = self.__senate2Info['depiction']['imageUrl']
            self.senate2['bio']['full_name'] = self.__senate2Info['directOrderName']
            self.senate2['state'] = self.__senate2Info['state']
            self.senate2['sponsoredLegislationCount'] = self.__senate2Info['sponsoredLegislation']['count']
            self.senate2['cosponsoredLegislationCount'] = self.__senate2Info['cosponsoredLegislation']['count']
            self.senate2['terms'] = self.__senate2Info['terms']
            self.senate2['typeSince'] = RepInfo.findYearOfOffice(self.senate2)

            # clean up memory and reduce object json output
            del self.__senate1Info, self.__senate2Info

        # clean up memory and reduce object json output
        del self.__houseInfo

    # my data doesn't tell me when the rep started in his office
    # so I get the info myself by looping through his list to find when it changes
    # this is helpful for reps who have moved from house to senate or vice versa
    @staticmethod
    def findYearOfOffice(rep):
        # check chamber instead of rep type because some territories (PR, DC) have delegates or commissioners instead of reps
        currentChamber = 'House of Representatives' if (rep['type'] == 'Representative' or 'Resident Commissioner' or 'Delegate') else 'Senate'
        n = 0
        # start at end of list and move back to see when it changes
        for i in reversed(rep['terms']):
            if i['chamber'] == currentChamber:
                n = n + 1
    
        return(rep['terms'][len(rep['terms']) - n]['startYear'])

    # pull info from congress API
    @staticmethod
    def getMemberInfo(bioguideId):
        # eval casts the JSON to a dict
        # get extra information from api.congress.gov. Not super helpful now, but will use this API
        #   to get bill information
        return eval(congress.get(CONGRESS_API + '/member/' + bioguideId).content)['member']

    @staticmethod
    def getMemberLegislation(bioguideId, legislationType):
        if legislationType == LegislationTypeEnum.SPONSORED:
            return eval(congress.get(CONGRESS_API + '/member/' + bioguideId + '/' + 'sponsored-legislation?limit=10').content)['sponsoredLegislation']
        elif legislationType == LegislationTypeEnum.COSPONSORED:
            return eval(congress.get(CONGRESS_API + '/member/' + bioguideId + '/' + 'cosponsored-legislation?limit=10').content)['cosponsoredLegislation']
        # else:
        #     return [ ]

# add api endpoint
class AddressCongress(Resource):
    def get(self, address=None):
        # error handling if a bad address is inputted
        try:
            # roundabout way of mangling the geocodio api to give me the congressional districts!
            result = client.geocode(address, fields=['cd'])
            congressReps = result['results'][0]['fields']['congressional_districts'][0]
            address = result['input']['formatted_address']

            return RepInfo(congressReps['name'], congressReps['ocd_id'], congressReps['current_legislators'], address).toJSON(), 200

        except:
            return "address not valid", 404


# add api endpoint
class MemberFetch(Resource):
    def get(self, bioguide=None):
        # useful for the congressman info page.
        rep = RepInfo.getMemberInfo(bioguide);
        rep['sponsoredLegislation']['recent'] = RepInfo.getMemberLegislation(bioguide, LegislationTypeEnum.SPONSORED)
        rep['cosponsoredLegislation']['recent'] = RepInfo.getMemberLegislation(bioguide, LegislationTypeEnum.COSPONSORED)
        rep['type'] = rep['terms'][-1]['memberType']
        rep['typeSince'] = RepInfo.findYearOfOffice(rep);
        return rep;
