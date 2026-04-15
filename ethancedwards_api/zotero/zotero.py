#!/usr/bin/env python3

import json, pyzotero, random, os
from flask_restful import Api, Resource, reqparse



ZOTERO_KEY = os.environ['ZOTERO_KEY']
LIB_ID = os.environ['LIB_ID']


from pyzotero import Zotero
zot = Zotero(LIB_ID, 'user', ZOTERO_KEY)  # local=True for read access to local Zotero

parser = reqparse.RequestParser()
parser.add_argument('library', required=True, type=str, location='args')

allowed_libraries = [
        {
            "slug": "ai",
            "name": "Ethan's AI Reading List",
            "description": "AI is incredibly consequential for our society. Here's what I read to help me think about it.",
            "collection": "LMI7UUEE",
        },
        {
            "slug": "cs2620",
            "name": "CS 2620",
            "description": "Here are some of the papers we read in CS 2620.",
            "collection": "ND7X873Z",
        },
        {
            "slug": "cs1610",
            "name": "CS 1610",
            "description": "Here are some of the papers we read in CS 1610.",
            "collection": "EGHNTF8X",
        },
        {
            "slug": "hsrg",
            "name": "Harvard Systems Reading Group",
            "description": "Here are some of the papers we read in the HSRG.",
            "collection": "7358XAIZ",
        },
        {
            "slug": "personalphil",
            "name": "Philosophy Readings",
            "description": "I'm a hobbyist philosophy reader, here are some papers I have read.",
            "collection": "PYWLUTYE",
        },
        {
            "slug": "technical",
            "name": "Interesting Technical Readings",
            "description": "The rise of AI has made me appreciate the importance of deep expertise even more. Here’s what I’m reading to learn.",
            "collection": "P5PJ8KPF",
        },
]

permed = [ ]

class Reading:
    def __init__(self,
                 title,
                 authors,
                 link,
                 date,
                 tags,
                 dateAdded
                 ):
        self.title = title
        self.author = authors
        self.link = link
        self.date = date
        self.tags = tags
        self.dateAdded = dateAdded

    def toJSON(self):
        return self.__dict__

def getReadings(library: str):
    items = zot.collection_items_top(library)

    readings = [ ]

    for item in items:
        entry = item['data']
        readings.append(Reading(title=entry.get('title'),
                          authors=entry.get('creators'),
                          link=entry.get('url'),
                          date=entry.get('date'),
                          tags=entry.get('tags'),
                          dateAdded=entry.get('dateAdded')
                        ).toJSON())

    return readings


class Libraries(Resource):
    def get(self):
        return allowed_libraries, 200

class Readings(Resource):
    def get(self):
        # this is the worst code ive ever written in my life
        args = parser.parse_args()

        if len(permed) == 0:
            for lib in allowed_libraries:
                permed.append(lib['slug'])

        lib = args['library']

        if lib not in permed:
            return "access denied", 403

        ind = -1

        for i in range(len(allowed_libraries)):
            if allowed_libraries[i]['slug'] == lib:
                ind = i
                del i # safety
                break

        if ind == -1:
            return "not found", 404

        readings = allowed_libraries[ind]

        readings['list'] = getReadings(allowed_libraries[ind]['collection'])

        return readings, 200
