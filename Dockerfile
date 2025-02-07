FROM python:alpine

RUN apk update && apk add --no-cache ffmpeg uv clang gcompat
WORKDIR /app
COPY ./pyproject.toml ./README.md /app/
RUN uv sync
COPY . /app
CMD ["uv", "run", "start"]
