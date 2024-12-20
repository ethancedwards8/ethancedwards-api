from flask import Flask
from flask_restful import Api, Resource, reqparse, fields
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
        'preferredcodec': 'mp3',
    }],
    "outtmpl": 'src/static/' + '%(id)s.%(ext)s'
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

def downloadAudio(link):
    ydl.download(link)

feed = podgen.Podcast(name="Ethan's Misc. Listening", 
                        description="Things that Ethan wants to listen to",
                        website="https://ethancedwards.com",
                        explicit=False,
                        withhold_from_itunes=True,
                        image="https://ethancedwards.com/logo.jpg")


def updateFile(feed):
    with open('src/static/feed.xml', 'w') as feed_file:
        feed_file.write(feed.rss_str())

parser = reqparse.RequestParser()
parser.add_argument('link', required=True, type=str, location='args')

linkList = [ ]

fields = {
        'link': fields.Url()
}

class AudioFeed(Resource):
    def get(self):
        return linkList

    def post(self):
        args = parser.parse_args()

        link = args['link']

        linkList.append(link)

        info_dict = ydl.extract_info(link, download=True)

        media_file = 'https://api.ethancedwards.com/static/' + info_dict['id'] + '.mp3'

        feed.episodes += [
                Episode(title=info_dict['title'],
                        media=podgen.Media.create_from_server_response(media_file),
                        summary=info_dict['description'])
        ]

        updateFile(feed)
        
        return {"message": "success"}, 200
