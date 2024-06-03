FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev libfontconfig1 libx11-xcb1 && \
    apt-get clean

RUN pip install pygame

WORKDIR /workspace

# 애플리케이션 소스 복사
COPY . /workspace

