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

# setup requests to FEC campgain finance api
FEC_API = "https://api.open.fec.gov/v1"
fec = requests.Session()
fec.params = { "format": "json" }
fec.headers.update({ "x-api-key": CONGRESS_KEY })

# setup requests for geocodio
client = GeocodioClient(GEO_KEY)

# make json -> dict work. Is there a better way?
true = True
false = False
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
        self.house = RepInfo.reshapeLegislatorInfo(reps[0])

        # for DC, PR, territories, etc, who don't have senators
        if len(reps) > 1:
            self.senate1 = RepInfo.reshapeLegislatorInfo(reps[1])
            self.senate2 = RepInfo.reshapeLegislatorInfo(reps[2])


    @staticmethod
    def reshapeLegislatorInfo(legislator):
        # storing the object to reduce the amount of requests needed
        legislatorInfo = RepInfo.getMemberInfo(legislator['references']['bioguide_id'])

        # add pictures and terms of each member
        legislator['type'] = legislator['type'].capitalize()
        legislator['picture'] = legislatorInfo['depiction']['imageUrl']
        legislator['bio']['full_name'] = legislatorInfo['directOrderName']
        legislator['state'] = legislatorInfo['state']
        legislator['sponsoredLegislationCount'] = legislatorInfo['sponsoredLegislation']['count']
        legislator['cosponsoredLegislationCount'] = legislatorInfo['cosponsoredLegislation']['count']
        legislator['terms'] = legislatorInfo['terms']
        legislator['typeSince'] = RepInfo.findYearOfOffice(legislator)

        # del legislatorInfo

        return legislator

    # my data doesn't tell me when the rep started in his office
    # so I get the info myself by looping through his list to find when it changes
    # this is helpful for reps who have moved from house to senate or vice versa
    @staticmethod
    def findYearOfOffice(rep):
        # check chamber instead of rep type because some territories (PR, DC) have delegates or commissioners instead of reps
        currentChamber = 'House of Representatives' if ((rep['type'] in { 'Representative', 'Resident Commissioner', 'Delegate' })) else 'Senate'
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
    def getMemberFinance(state, district, office, year):
        officeLetter = 'H' if office in { 'Representative', 'Resident Commissioner', 'Delegate' } else 'S'
        # use office info to determine the occupants FEC id. Should be able to remove once Geocodio API changes.
        candidateID = eval(congress.get(FEC_API + '/candidates/search/?page=1&per_page=2&incumbent_challenge=I&sort=-election_years&office=' + officeLetter + '&state=' + state + '&district=' + str(district) + '&election_year=' + str(year)).content)['results'][0]['candidate_id']
        # use FEC ID to pull latest finance info
        candidateFinances = eval(congress.get(FEC_API + '/candidate/' + candidateID + '/totals').content)['results'][0]
        return candidateFinances

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
        rep['finance'] = RepInfo.getMemberFinance(rep['terms'][-1]['stateCode'], rep['terms'][-1]['district'] if 'district' in rep['terms'][-1] else '00', rep['terms'][-1]['memberType'], int(rep['typeSince']) - 1)
        return rep

# result = client.geocode('1600 Pennsylvania Ave, Washington DC, DC 20500', fields=['cd'])
# congressReps = result['results'][0]['fields']['congressional_districts'][0]
# testRep = RepInfo(congressReps['name'], congressReps['ocd_id'], congressReps['current_legislators'], '1600 Pennsylvania Ave, Washington DC, DC 20500').toJSON()
# print(json.dumps(testRep))
# address = result['input']['formatted_address']

# print(json.dumps(RepInfo.getMemberFinance('VA', '00', 'Senate', 2008)))

# bioguide = 'P000610'
# testRep = RepInfo.getMemberInfo(bioguide)
# testRep['sponsoredLegislation']['recent'] = RepInfo.getMemberLegislation(bioguide, LegislationTypeEnum.SPONSORED)
# testRep['cosponsoredLegislation']['recent'] = RepInfo.getMemberLegislation(bioguide, LegislationTypeEnum.COSPONSORED)
# testRep['type'] = testRep['terms'][-1]['memberType']
# testRep['typeSince'] = RepInfo.findYearOfOffice(testRep);
# testRep['finance'] = RepInfo.getMemberFinance(testRep['terms'][-1]['stateCode'], testRep['terms'][-1]['district'] if 'district' in testRep['terms'][-1] else '00', testRep['terms'][-1]['memberType'], int(testRep['typeSince']) - 1)

# print(testRep['finance'])
