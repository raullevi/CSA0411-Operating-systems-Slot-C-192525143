#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

chmod +x access_log_summary.sh disk_alert.sh

echo "=========================================================="
echo "Executing Task B1: Linux Administration & Log Analysis..."
echo "=========================================================="
{
    echo "--- 1. Verification of access_log_summary.sh (TODO 1 & 2) ---"
    ./access_log_summary.sh
    echo ""
    echo "--- 2. Crontab Schedule Configuration ---"
    echo "0 * * * * /var/www/result-portal/access_log_summary.sh >> /var/log/traffic.log 2>&1"
    echo ""
    echo "--- 3. Automated Disk Alert Verification ---"
    ./disk_alert.sh
} | tee experiment_b1_results.log

echo ""
echo "Task B1 execution finished successfully."
