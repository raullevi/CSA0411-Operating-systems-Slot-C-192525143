#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 06: Cost of System Calls (copy_file)..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running copy_file_todo and logging output..."
./copy_file_todo | tee experiment_q6_results.log

echo ""
echo "Task 06 execution finished successfully."
