from flask import Flask
from flask_restful import Api, Resource, reqparse, fields
from podgen import Episode, Media

import yt_dlp

import json
import os
import sys

currentDir = os.path.dirname(sys.argv[0])

ydl_opts = {
    'format': 'mp3',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    # 'postprocessors': [{  # Extract audio using ffmpeg
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'm4a',
    # }],
    "outtmpl": currentDir + '/static/' + '%(id)s.%(ext)s'
}

class Video():
    # nice to have
    def toJSON(self):
        return self.__dict__

    def __init__(self, title, video, summary, link)
        self.title = title
        self.video = video
        self.summary = summary
        self.link = link

videos = [ ]

ydl = yt_dlp.YoutubeDL(ydl_opts)

def downloadVideo(link):
    ydl.download(link)

parser = reqparse.RequestParser()
parser.add_argument('link', required=True, type=str, location='args')

class VideoServer(Resource):
    def get(self):
        return videos

    def post(self):
        args = parser.parse_args()

        link = args['link']

        info_dict = ydl.extract_info(link, download=True)

        media_file = 'https://api.ethancedwards.com/static/' + info_dict['id'] + '.m4a'

        videos += [
            Video(title==info_dict['title'],
                  video=)
        ]


