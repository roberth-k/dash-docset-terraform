# Use a slim Python image with common build tools for make docset
FROM python:3.11-slim-bookworm

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        make \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["make"]
CMD ["docset"]
