#!/usr/bin/env python3

import json, pyzotero, random, os
from flask_restful import Api, Resource, reqparse



ZOTERO_KEY = os.environ['ZOTERO_KEY']
LIB_ID = os.environ['LIB_ID']
COL_ID = os.environ['COL_ID']


from pyzotero import Zotero
zot = Zotero(LIB_ID, 'user', ZOTERO_KEY)  # local=True for read access to local Zotero


class Reading:
    def __init__(self, title, authors, link, date):
        self.title = title
        self.author = authors
        self.link = link
        self.date = date

    def toJSON(self):
        return self.__dict__

def getReadings():
    items = zot.collection_items_top("LMI7UUEE")

    readings = [ ]

    for item in items:
        entry = item['data']
        readings.append(Reading(title=entry.get('title'),
                          authors=entry.get('creators'),
                          link=entry.get('url'),
                          date=entry.get('date')
                        ).toJSON())

    return readings


class Readings(Resource):
    def get(self):
        readings = getReadings()
        return readings, 200
