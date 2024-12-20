from flask import Flask
from flask_restful import Api, Resource, reqparse
from podgen import Episode, Media
import podgen
import yt_dlp

import json
import os

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

def downloadAudio(link):
    ydl.download(link)

feed = podgen.Podcast(name="Ethan's Misc. Listening", 
                        description="Things that Ethan wants to listen to",
                        website="https://ethancedwards.com",
                        explicit=False,
                        withhold_from_itunes=True)


linkList = [ ]

class AudioFeed(Resource):
    def get(self, link):
        if link == "dump":
            return feed.rss_str(), 200
        else:
            return "sorry, not found", 404

    def post(self, link):
        linkList.append(link)
        
        return {"message": "success"}, 200


