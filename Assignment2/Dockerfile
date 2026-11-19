# Dockerfile for CSA0411 Operating Systems Assignment 2 (CO2)
# Student: Rakul K (Reg No: 192525143)

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    python3 \
    python3-pip \
    strace \
    time \
    procps \
    git \
    valgrind \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY . /workspace

RUN chmod +x run_all_tasks.sh Task*/run_q*.sh

CMD ["/bin/bash", "./run_all_tasks.sh"]
