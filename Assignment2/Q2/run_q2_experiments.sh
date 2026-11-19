#!/bin/bash
# run_q2_experiments.sh - Automated execution script for Task 02
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 02: CPU Scheduling Suite & Complete Code..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running cpu_scheduling_todo and cpu_scheduler_suite..."
{
    echo "=========================================================="
    echo "1. VERIFICATION OF COMPLETE THE CODE (EXACT PDF MATCH)"
    echo "=========================================================="
    ./cpu_scheduling_todo
    echo ""
    echo "=========================================================="
    echo "2. FULL SCHEDULING SUITE & QUANTUM STUDY"
    echo "=========================================================="
    ./cpu_scheduler_suite
} | tee experiment_q2_results.log

echo ""
echo "Task 02 execution finished successfully."
