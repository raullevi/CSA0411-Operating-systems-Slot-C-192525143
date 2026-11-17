#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

LOG="experiment_q6_results.log"
exec > >(tee "$LOG") 2>&1

echo "=========================================================================="
echo "  CSA0411 OS ASSIGNMENT 3 - QUESTION 6 DISK MANAGEMENT EXPERIMENTS"
echo "  Student: Rakul K | Register Number: 192525143"
echo "  Date: $(date)"
echo "=========================================================================="

echo -e "\n[STEP 1] Building Q6 Disk Programs..."
make clean
make

echo -e "\n[STEP 2] Running RAID Capacity & Data Loss Probability Calculator:"
./raid_calculator

echo -e "\n[STEP 3] Running Disk I/O Storage Benchmark (Sequential & Random Reads):"
./disk_benchmark

echo -e "\n[STEP 4] Showing System Partitions and Swap Configuration:"
if command -v lsblk >/dev/null 2>&1; then
    echo "--- Linux lsblk output ---"
    lsblk || true
    echo "--- Linux fdisk -l output ---"
    fdisk -l 2>/dev/null || true
    echo "--- Linux swap summary ---"
    swapon --show 2>/dev/null || true
elif command -v diskutil >/dev/null 2>&1; then
    echo "--- macOS diskutil partition list ---"
    diskutil list || true
    echo "--- macOS swap summary ---"
    sysctl vm.swapusage || true
fi

echo -e "\n=========================================================================="
echo "  QUESTION 6 EXPERIMENTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
