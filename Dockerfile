FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY atlas_engine /app/atlas_engine
COPY src /app/src
COPY default /app/default
COPY config.py /app/config.py
COPY chunk_registry.json /app/chunk_registry.json
COPY README.md /app/README.md

RUN mkdir -p /app/.env /app/chat_history

ENTRYPOINT ["python"]
CMD ["src/gemini_rag.py", "--backend", "gemini"]
