#!/usr/bin/env bash
# run_all_tasks.sh - Master execution script for CSA0411 Assignment 2 (CO2)
# Student: Rakul K | Register Number: 192525143

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

echo "======================================================================"
echo "  SIMATS ENGINEERING - DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
echo "  CSA0411 / CSA04 - OPERATING SYSTEMS (SLOT C)"
echo "  ASSIGNMENT 2 (CO2) - COMPLETE VERIFICATION & EVALUATION RUNNER"
echo "  Student: Rakul K | Register Number: 192525143"
echo "======================================================================"
echo ""

TASKS=(
    "Task01_Processes_and_States/run_q1_experiments.sh"
    "Task02_CPU_Scheduling/run_q2_experiments.sh"
    "Task03_POSIX_Threads/run_q3_experiments.sh"
    "Task04_IPC_Pipelines/run_q4_experiments.sh"
    "Task05_Synchronization_Primitives/run_q5_experiments.sh"
    "Task06_Deadlock_Bankers/run_q6_experiments.sh"
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
echo "  ALL 6 TASKS COMPILED, EXECUTED, LOGGED AND SCREENSHOTTED SUCCESSFULLY!"
echo "======================================================================"
