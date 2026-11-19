#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 04: Disk Scheduling Algorithms..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running disk_sched_todo and disk_sim_suite..."
{
    echo "=========================================================="
    echo "1. VERIFICATION OF COMPLETE THE CODE (DISK SCHEDULING)"
    echo "=========================================================="
    ./disk_sched_todo
    echo ""
    echo "=========================================================="
    echo "2. EXTENDED DISK SIMULATION & STARVATION ANALYSIS"
    echo "=========================================================="
    ./disk_sim_suite
} | tee experiment_q4_results.log

echo ""
echo "Task 04 execution finished successfully."
