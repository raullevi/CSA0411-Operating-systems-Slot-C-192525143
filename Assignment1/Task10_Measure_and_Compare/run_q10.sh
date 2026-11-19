#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 10: Measurement & Comparison (bench)..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running measure_bench and logging output..."
./measure_bench | tee experiment_q10_results.log

echo ""
echo "Task 10 execution finished successfully."
