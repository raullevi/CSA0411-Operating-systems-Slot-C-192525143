#!/bin/bash
# run_q3_experiments.sh - Automated execution script for Task 03
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 03: POSIX Threads & Traffic Camera Sim..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running camera_threads and logging output..."
./camera_threads | tee experiment_q3_results.log

echo ""
echo "Task 03 execution finished successfully."
