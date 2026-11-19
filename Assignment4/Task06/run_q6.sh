#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 06: Video Storage Simulation Suite..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running video_storage_sim and logging output..."
./video_storage_sim | tee experiment_q6_results.log

echo ""
echo "Task 06 execution finished successfully."
