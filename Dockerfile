FROM python:alpine

RUN apk update && apk add --no-cache ffmpeg uv clang
WORKDIR /app
COPY ./pyproject.toml ./README.md /app/
RUN uv sync
COPY . /app
ENTRYPOINT ["uv", "run", "start"]
