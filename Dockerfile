FROM python:alpine

RUN apk update && apk add --no-cache ffmpeg poetry
WORKDIR /app
COPY . /app
RUN poetry install
ENTRYPOINT ["poetry", "run", "start"]
