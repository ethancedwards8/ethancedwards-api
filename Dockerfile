FROM python
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get -y install ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN uv sync --frozen --compile-bytecode --no-dev
ENTRYPOINT ["uv", "run", "start"]
