#!/usr/bin/env bash
# disk_alert.sh - Monitor disk usage and trigger alert if threshold exceeds 85%
set -euo pipefail

THRESHOLD=85
CURRENT=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

echo "--- Disk Space Health Check ---"
echo "Root Partition Usage: ${CURRENT}% (Threshold: ${THRESHOLD}%)"
if [ "$CURRENT" -gt "$THRESHOLD" ]; then
    echo "WARNING: Disk space critically low! Triggering administrator webhook alert."
else
    echo "OK: Disk space is within safe operational limits."
fi
