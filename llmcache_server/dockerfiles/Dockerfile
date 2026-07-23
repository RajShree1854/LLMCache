FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir llmcache

WORKDIR /workspace

CMD ["llmcache_server", "-s", "0.0.0.0"]
