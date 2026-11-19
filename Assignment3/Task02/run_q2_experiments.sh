#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

LOG="experiment_q2_results.log"
exec > >(tee "$LOG") 2>&1

echo "=========================================================================="
echo "  CSA0411 OS ASSIGNMENT 3 - QUESTION 2 PAGING EXPERIMENTS"
echo "  Student: Rakul K | Register Number: 192525143"
echo "  Date: $(date)"
echo "=========================================================================="

echo -e "\n[STEP 1] Building Q2 Programs (paging_todo and paging_sim)..."
make clean
make

echo -e "\n[STEP 2] Running 'Complete the Code' Program (paging_todo):"
./paging_todo

echo -e "\n[STEP 3] Running Multi-User College Server Simulation (paging_sim):"
./paging_sim

echo -e "\n[STEP 4] System Environment Page Size and Measurement:"
echo -n "Operating System getconf PAGESIZE: "
getconf PAGESIZE || true
echo -n "Operating System pagesize command: "
pagesize || true

echo -e "\n[STEP 5] Timing and Page Fault Measurement of Execution (/usr/bin/time):"
/usr/bin/time -l ./paging_todo 2>&1 | grep -E "page|resident|real|user|sys" || true

echo -e "\n=========================================================================="
echo "  QUESTION 2 EXPERIMENTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
