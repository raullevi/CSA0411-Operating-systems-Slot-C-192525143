#!/usr/bin/env bash
# run_all_tasks.sh - Master execution script for CSA0411 Assignment 1 (CO1)
# Student: Rakul K | Register Number: 192525143

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

echo "======================================================================"
echo "  SIMATS ENGINEERING - DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
echo "  CSA0411 / CSA04 - OPERATING SYSTEMS (SLOT C)"
echo "  ASSIGNMENT 1 (CO1) - SMART HOSPITAL OS EVALUATION RUNNER"
echo "  Student: Rakul K | Register Number: 192525143"
echo "======================================================================"
echo ""

TASKS=(
    "Task06_Cost_of_System_Calls/run_q6.sh"
    "Task07_Process_Control/run_q7.sh"
    "Task10_Measure_and_Compare/run_q10.sh"
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
echo "  ALL ASSIGNMENT 1 TASKS EXECUTED, VERIFIED AND LOGGED SUCCESSFULLY!"
echo "======================================================================"
