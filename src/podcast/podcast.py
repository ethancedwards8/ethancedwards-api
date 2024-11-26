#!/usr/bin/env python3

import json, feedparser, random
from flask_restful import Api, Resource, reqparse

URL = "https://theridgepodcast.com/feed/podcast"

feed = feedparser.parse(URL)

class Episode:
    def __init__(self, index, title, date):
        self.index = index
        self.title = title
        self.date = date
    def toJSON(self):
        return self.__dict__

podcast = [ ]

i = len(feed.entries)
count = i

for entry in feed.entries:
    podcast.append(Episode(i, entry.title, entry.published).toJSON())
    i -= 1

class Podcast(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(podcast), 200

        episode = podcast[count - id]
        if episode:
            return episode, 200, {'Access-Control-Allow-Origin': '*'}

        return "quote not found", 404

class PodcastDump(Resource):
    def get(self):
        return podcast, 200

