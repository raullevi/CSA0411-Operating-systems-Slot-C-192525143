#!/bin/bash
# run_q4_experiments.sh - Automated execution script for Task 04
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 04: IPC Pipelines & Benchmark..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running pipe_ipc_todo and ipc_comparison_bench..."
{
    echo "=========================================================="
    echo "1. VERIFICATION OF COMPLETE THE CODE (PIPE IPC)"
    echo "=========================================================="
    ./pipe_ipc_todo
    echo ""
    echo "=========================================================="
    echo "2. IPC THROUGHPUT BENCHMARK (PIPE VS SHM)"
    echo "=========================================================="
    ./ipc_comparison_bench
} | tee experiment_q4_results.log

echo ""
echo "Task 04 execution finished successfully."
