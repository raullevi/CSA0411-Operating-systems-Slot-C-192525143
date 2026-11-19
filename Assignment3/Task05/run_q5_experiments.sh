#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

LOG="experiment_q5_results.log"
exec > >(tee "$LOG") 2>&1

echo "=========================================================================="
echo "  CSA0411 OS ASSIGNMENT 3 - QUESTION 5 PAGE REPLACEMENT EXPERIMENTS"
echo "  Student: Rakul K | Register Number: 192525143"
echo "  Date: $(date)"
echo "=========================================================================="

echo -e "\n[STEP 1] Building Q5 Page Replacement Programs..."
make clean
make

echo -e "\n[STEP 2] Running 'Complete the Code' Program (page_replacement_todo):"
./page_replacement_todo

echo -e "\n[STEP 3] Running Full Replacement Suite (FIFO, LRU, Clock, Optimal, 100k Benchmark):"
./replacement_engine

echo -e "\n[STEP 4] Generating Comparative Faults vs Frames SVG Plot:"
python3 plot_replacement.py

echo -e "\n=========================================================================="
echo "  QUESTION 5 EXPERIMENTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
