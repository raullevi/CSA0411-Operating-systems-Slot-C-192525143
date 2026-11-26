#!/bin/bash 
SRC=project 
BACKUP_DIR=backup 
mkdir -p $SRC $BACKUP_DIR 
echo "main program" > $SRC/main.c 
echo "notes" > $SRC/notes.txt 
  
FILE=$BACKUP_DIR/${SRC}_$(date +%Y%m%d_%H%M%S).tar.gz 
tar -czf $FILE $SRC 
echo "Backup created : $FILE" 
echo "Archive contents:" 
tar -tzf $FILE 
  
rm -rf $SRC 
echo "Original directory deleted (simulated data loss)" 
ls $SRC 2>/dev/null || echo "$SRC not found" 
  
tar -xzf $FILE 
echo "Restored from backup. Files:" 
ls -l $SRC
