# Dockerfile for CSA0411 Operating Systems Assignment 3 (CO3)
# Student: Rakul K | Register Number: 192525143

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install core build toolchains, debuggers, profiling tools, and Python
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    gdb \
    time \
    util-linux \
    python3 \
    python3-pip \
    libbsd-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all project tasks and sources
COPY . /app

# Ensure all experiment runner scripts are executable
RUN chmod +x run_all_tasks.sh \
    Q1_Linking_Loading/run_q1_experiments.sh \
    Q2_Paging/run_q2_experiments.sh \
    Q3_Segmentation/run_q3_experiments.sh \
    Q4_Virtual_Memory/run_q4_experiments.sh \
    Q5_Page_Replacement/run_q5_experiments.sh \
    Q6_Disk_Management/run_q6_experiments.sh \
    Q7_Memory_Management_Plan/run_q7_experiments.sh

# Default container execution: run the entire OS assignment test suite
CMD ["/app/run_all_tasks.sh"]
