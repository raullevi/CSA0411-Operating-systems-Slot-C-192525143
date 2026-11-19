#!/bin/bash
# run_q1_experiments.sh - Automated execution script for Task 01
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 01: Processes & Process States Simulation..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running process_tree_sim and logging output to experiment_q1_results.log..."
./process_tree_sim | tee experiment_q1_results.log

echo ""
echo "Task 01 execution finished successfully."
