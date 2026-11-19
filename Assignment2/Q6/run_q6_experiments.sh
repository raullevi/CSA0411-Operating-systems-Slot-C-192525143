#!/bin/bash
# run_q6_experiments.sh - Automated execution script for Task 06
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 06: Banker's Algorithm & Scaling Suite..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running bankers_todo and bankers_scale_bench..."
{
    echo "=========================================================="
    echo "1. VERIFICATION OF COMPLETE THE CODE (BANKER'S ALGORITHM)"
    echo "=========================================================="
    ./bankers_todo
    echo ""
    echo "=========================================================="
    echo "2. BANKER'S SCALABILITY BENCHMARK (N=10, 100, 1000)"
    echo "=========================================================="
    ./bankers_scale_bench
} | tee experiment_q6_results.log

echo ""
echo "Task 06 execution finished successfully."
