FROM python:alpine

RUN apk update && apk add --no-cache ffmpeg
RUN pip3 install flask flask-restful feedparser requests pygeocodio yt-dlp podgen
COPY . /app
ENTRYPOINT ["python3", "/app/src/ethancedwards_api.py"]
