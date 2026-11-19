#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

LOG="experiment_q3_results.log"
exec > >(tee "$LOG") 2>&1

echo "=========================================================================="
echo "  CSA0411 OS ASSIGNMENT 3 - QUESTION 3 SEGMENTATION EXPERIMENTS"
echo "  Student: Rakul K | Register Number: 192525143"
echo "  Date: $(date)"
echo "=========================================================================="

echo -e "\n[STEP 1] Building Q3 Segmentation Simulator..."
make clean
make

echo -e "\n[STEP 2] Executing Segmentation Suite (Translation, SIGSEGV, Frag Sim):"
./segmentation_sim

echo -e "\n[STEP 3] Inspecting Running Process Virtual Memory Segments:"
if [ -f "/proc/$$/maps" ]; then
    echo "Linux /proc/$$/maps for shell:"
    head -n 20 "/proc/$$/maps"
elif command -v vmmap >/dev/null 2>&1; then
    echo "macOS vmmap segment breakdown for current shell (PID $$):"
    vmmap -summary $$ | grep -E "REGION TYPE|__TEXT|__DATA|Stack|MALLOC|TOTAL" || true
else
    ps -o pid,vsz,rss,comm -p $$
fi

echo -e "\n=========================================================================="
echo "  QUESTION 3 EXPERIMENTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
