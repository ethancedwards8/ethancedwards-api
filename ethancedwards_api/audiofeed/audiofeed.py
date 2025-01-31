from flask import Flask
from flask_restful import Api, Resource, reqparse, fields
from podgen import Episode, Media
import podgen
import yt_dlp

import json
import os
import sys

currentDir = os.path.dirname(sys.argv[0])

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }],
    "outtmpl": currentDir + '/static/' + '%(id)s.%(ext)s'
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

def downloadAudio(link):
    ydl.download(link)

# https://stackoverflow.com/questions/74188289/how-do-i-parse-xml-rss-feed-content-in-python
# import after restart sol. maybe? will try later
feed = podgen.Podcast(name="Ethan's Misc. Listening", 
                        description="Things that Ethan wants to listen to",
                        website="https://ethancedwards.com",
                        explicit=False,
                        withhold_from_itunes=True,
                        image="https://ethancedwards.com/logo.jpg")


def updateFile(feed):
    with open(currentDir + '/static/feed.xml', 'w') as feed_file:
        feed_file.write(feed.rss_str())

parser = reqparse.RequestParser()
parser.add_argument('link', required=True, type=str, location='args')

class AudioFeed(Resource):
    def get(self):
        temp = [ ]
        for episode in feed.episodes:
            temp.append(episode.title)
        return temp

    def post(self):
        args = parser.parse_args()

        link = args['link']

        info_dict = ydl.extract_info(link, download=True)

        media_file = 'https://api.ethancedwards.com/static/' + info_dict['id'] + '.m4a'

        feed.episodes += [
                Episode(title=info_dict['title'],
                        media=podgen.Media.create_from_server_response(media_file),
                        summary=info_dict['description'])
        ]

        updateFile(feed)
        
        return {"message": "success, added episode " + info_dict['title']}, 200
