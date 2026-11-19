#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Compiling Task 07: Process Control System Calls (shell)..."
echo "=========================================================="
make clean
make all

echo ""
echo "Running shell_todo and logging output..."
./shell_todo | tee experiment_q7_results.log

echo ""
echo "Task 07 execution finished successfully."
