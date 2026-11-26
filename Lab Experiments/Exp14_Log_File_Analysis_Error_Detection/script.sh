#!/bin/bash 
LOG=app.log 
cat > $LOG << EOF 
2025-08-01 10:00:01 INFO  Server started 
2025-08-01 10:02:15 WARNING Disk usage 85% 
2025-08-01 10:05:40 ERROR Database connection failed 
2025-08-01 10:06:02 INFO  Retrying connection 
2025-08-01 10:06:30 ERROR Database connection failed 
2025-08-01 10:10:11 ERROR File not found: config.ini 
2025-08-01 10:12:45 INFO  Request served 
EOF 
  
echo "Log file      : $LOG" 
echo "Total lines   : $(wc -l < $LOG)" 
echo "INFO lines    : $(grep -c 'INFO' $LOG)" 
echo "WARNING lines : $(grep -c 'WARNING' $LOG)" 
echo "ERROR lines   : $(grep -c 'ERROR' $LOG)" 
echo 
echo "Error lines with line numbers:" 
grep -n "ERROR" $LOG 
echo 
echo "Most frequent error:" 
grep "ERROR" $LOG | cut -d' ' -f4- | sort | uniq -c | sort -nr | head -1
