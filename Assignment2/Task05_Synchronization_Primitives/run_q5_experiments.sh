#!/bin/bash
# run_q5_experiments.sh - Automated execution script for Task 05
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 05: Synchronization Primitives Suite..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running sync_todo, 100-run verification, and railway_booking_sim..."
{
    echo "=========================================================="
    echo "1. VERIFICATION OF COMPLETE THE CODE (BOUNDED BUFFER)"
    echo "=========================================================="
    ./sync_todo
    echo ""
    echo "=========================================================="
    echo "2. 100-RUN DETERMINISM VERIFICATION"
    echo "=========================================================="
    for i in {1..100}; do
        res=$(./sync_todo)
        if [[ "$res" != "items consumed: 20, sum = 210 (expected 210)" ]]; then
            echo "FAILED at iteration $i: $res"
            exit 1
        fi
    done
    echo "Verification Passed: 100/100 runs produced exact expected sum 210 with zero race conditions!"
    echo ""
    echo "=========================================================="
    echo "3. RAILWAY LOCKING GRANULARITY & PRIMITIVES BENCHMARK"
    echo "=========================================================="
    ./railway_booking_sim
} | tee experiment_q5_results.log

echo ""
echo "Task 05 execution finished successfully."
