#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

LOG="experiment_q7_results.log"
exec > >(tee "$LOG") 2>&1

echo "=========================================================================="
echo "  CSA0411 OS ASSIGNMENT 3 - QUESTION 7 MEMORY MANAGEMENT DESIGN EXPERIMENTS"
echo "  Student: Rakul K | Register Number: 192525143"
echo "  Date: $(date)"
echo "=========================================================================="

echo -e "\n[STEP 1] Building Q7 Real-Time and Edge Architecture Programs..."
make clean
make

echo -e "\n[STEP 2] Running Real-Time Memory Locking Benchmark (Unlocked vs mlock):"
./rt_memory_lock_benchmark

echo -e "\n[STEP 3] Running 3-Task Edge Device Memory Simulator & 4th-Task Analysis:"
./edge_device_memory_sim

echo -e "\n=========================================================================="
echo "  QUESTION 7 EXPERIMENTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
