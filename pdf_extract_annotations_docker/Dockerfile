# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
  python3-poppler-qt5 \
  && rm -rf /var/lib/apt/lists/*

COPY ../pdf_extract_annotations.py /app/
WORKDIR /tmp/
ENTRYPOINT [ "python3", "/app/pdf_extract_annotations.py" ]
