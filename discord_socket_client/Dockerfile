FROM ghcr.io/linuxserver/baseimage-ubuntu:focal

ENV BRANCH=wip-v0.0-initial-push

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    git && \
    mkdir -p /app && \
    cd /app && \
    git clone -b ${BRANCH} https://github.com/sohovercomplicated/Legion-Chatbot.git && \
    cd Legion-Chatbot/discord_socket_client && \
    pip install -U pip && \
    pip install -U setuptools wheel && \
    pip install -U -r requirements.txt

COPY root/ /




