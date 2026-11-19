#!/usr/bin/env bash
# run_all_tasks.sh - Master execution script for CSA0411 Assignment 4 (CO4)
# Student: Rakul K | Register Number: 192525143

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

echo "======================================================================"
echo "  SIMATS ENGINEERING - DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
echo "  CSA0411 / CSA04 - OPERATING SYSTEMS (SLOT C)"
echo "  ASSIGNMENT 4 (CO4) - OPTIMISING FILE STORAGE & DISK ACCESS RUNNER"
echo "  Student: Rakul K | Register Number: 192525143"
echo "======================================================================"
echo ""

TASKS=(
    "Task02_Workload_to_FileAllocation/run_q2.sh"
    "Task04_Disk_Scheduling_Algorithms/run_q4.sh"
    "Task06_Design_Challenge_Video_Streaming/run_q6.sh"
)

for script in "${TASKS[@]}"; do
    echo ">>> Executing $script..."
    bash "$script"
    echo ""
done

echo ">>> Regenerating terminal screenshot PNGs into output_ss/..."
python3 generate_terminal_screenshots.py

echo ""
echo "======================================================================"
echo "  ALL ASSIGNMENT 4 TASKS EXECUTED, VERIFIED AND LOGGED SUCCESSFULLY!"
echo "======================================================================"
