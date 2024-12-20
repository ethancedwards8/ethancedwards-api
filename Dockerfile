FROM python:alpine

COPY . /app
RUN apk update && apk add --no-cache ffmpeg
RUN pip3 install flask flask-restful feedparser requests pygeocodio yt-dlp podgen
ENTRYPOINT ["python3", "/app/src/ethancedwards_api.py"]
