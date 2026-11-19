#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

LOG="experiment_q4_results.log"
exec > >(tee "$LOG") 2>&1

echo "=========================================================================="
echo "  CSA0411 OS ASSIGNMENT 3 - QUESTION 4 VIRTUAL MEMORY EXPERIMENTS"
echo "  Student: Rakul K | Register Number: 192525143"
echo "  Date: $(date)"
echo "=========================================================================="

echo -e "\n[STEP 1] Building Q4 VM Experiments..."
make clean
make

echo -e "\n[STEP 2] Running Virtual Memory Experiments Suite:"
./vm_experiments

echo -e "\n[STEP 3] Generating Page Fault vs Frame Count SVG Curve:"
python3 plot_curve.py

echo -e "\n[STEP 4] Memory and Swap Status of Current System:"
if [ -f "/proc/meminfo" ]; then
    echo "Linux Memory and Swap Info:"
    grep -E "MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree" /proc/meminfo
elif command -v sysctl >/dev/null 2>&1; then
    echo "Host Physical Memory:"
    sysctl hw.memsize
    echo "Host VM Swap Usage:"
    sysctl vm.swapusage
fi

echo -e "\n=========================================================================="
echo "  QUESTION 4 EXPERIMENTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
