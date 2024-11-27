#!/usr/bin/env python3

import json, feedparser, random
from flask_restful import Api, Resource, reqparse

URL = "https://theridgepodcast.com/feed/podcast"


class Episode:
    def __init__(self, index, title, date, link):
        self.index = index
        self.title = title
        self.date = date
        self.link = link
    def toJSON(self):
        return self.__dict__

podcast = [ ]

count = len(podcast)

def getEps():
    print("request made")
    feed = feedparser.parse(URL)
    i = len(feed.entries)
    for entry in feed.entries:
        podcast.append(Episode(i, entry.title, entry.published, entry.link).toJSON())
        i -= 1

class Podcast(Resource):
    def get(self, id=0):
        getEps()
        # podcast/v1/0 returns a random episode
        if id == 0:
            return random.choice(podcast), 200

        episode = podcast[count - id]
        # returns episode X when /podcast/v1/X
        if episode:
            return episode, 200, {'Access-Control-Allow-Origin': '*'}

        return "episode not found", 404

class PodcastDump(Resource):
    def get(self):
        getEps()
        # returns list of all podcasts
        return podcast, 200

