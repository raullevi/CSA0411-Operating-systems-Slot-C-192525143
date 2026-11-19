#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 02: File Allocation Methods (NVR Sim)..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running file_alloc_todo and logging output..."
./file_alloc_todo | tee experiment_q2_results.log

echo ""
echo "Task 02 execution finished successfully."
