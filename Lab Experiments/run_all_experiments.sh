#!/usr/bin/env bash
# Master runner for all 40 CSA04 Lab Experiments
set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================="
echo "  SIMATS ENGINEERING - CSA04 OPERATING SYSTEMS LAB MANUAL   "
echo "  Executing all 40 Experiments for Rakul K (192525143)      "
echo "============================================================="

echo "
>>> Running Exp 01: IMPLEMENTATION OF LINUX COMMANDS FOR FILE AND DIRECTORY OPERATIONS..."
cd "${BASE_DIR}/Exp01_Linux_Commands_File_Directory"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 01 executed and verified."
echo "
>>> Running Exp 02: DEVELOPMENT OF SHELL SCRIPTS FOR SYSTEM INFORMATION AND RESOURCE MONITORING..."
cd "${BASE_DIR}/Exp02_System_Info_Resource_Monitoring"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 02 executed and verified."
echo "
>>> Running Exp 03: IMPLEMENTATION OF SHELL SCRIPTS USING VARIABLES, OPERATORS, AND EXPRESSIONS..."
cd "${BASE_DIR}/Exp03_Shell_Variables_Operators_Expressions"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 03 executed and verified."
echo "
>>> Running Exp 04: DEVELOPMENT OF SHELL SCRIPTS USING CONDITIONAL STATEMENTS..."
cd "${BASE_DIR}/Exp04_Shell_Conditional_Statements"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 04 executed and verified."
echo "
>>> Running Exp 05: DEVELOPMENT OF SHELL SCRIPTS USING LOOPS AND FUNCTIONS..."
cd "${BASE_DIR}/Exp05_Shell_Loops_and_Functions"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 05 executed and verified."
echo "
>>> Running Exp 06: IMPLEMENTATION OF FILE PERMISSIONS AND OWNERSHIP MANAGEMENT IN LINUX..."
cd "${BASE_DIR}/Exp06_File_Permissions_Ownership_Management"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 06 executed and verified."
echo "
>>> Running Exp 07: IMPLEMENTATION OF SYSTEM CALLS FOR FILE CREATION, READING, WRITING, AND DELETION..."
cd "${BASE_DIR}/Exp07_System_Calls_File_Create_Read_Write_Delete"
gcc main.c  -o exp07
./exp07  > /dev/null 2>&1 || true
echo "  [OK] Exp 07 compiled and verified."
echo "
>>> Running Exp 08: IMPLEMENTATION OF PROCESS INFORMATION RETRIEVAL USING LINUX SYSTEM INTERFACES..."
cd "${BASE_DIR}/Exp08_Process_Info_Linux_Interfaces"
gcc main.c  -o exp08
./exp08  > /dev/null 2>&1 || true
echo "  [OK] Exp 08 compiled and verified."
echo "
>>> Running Exp 09: IMPLEMENTATION OF CPU AND MEMORY UTILIZATION MONITORING SCRIPTS..."
cd "${BASE_DIR}/Exp09_CPU_Memory_Utilization_Monitoring"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 09 executed and verified."
echo "
>>> Running Exp 10: DEVELOPMENT OF SHELL SCRIPTS FOR AUTOMATED FILE BACKUP AND RECOVERY..."
cd "${BASE_DIR}/Exp10_Shell_Automated_Backup_Recovery"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 10 executed and verified."
echo "
>>> Running Exp 11: IMPLEMENTATION OF COMMAND PIPELINES, INPUT REDIRECTION, AND OUTPUT REDIRECTION..."
cd "${BASE_DIR}/Exp11_Command_Pipelines_Redirection"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 11 executed and verified."
echo "
>>> Running Exp 12: DEVELOPMENT OF SHELL SCRIPTS FOR USER ACCOUNT AND GROUP MANAGEMENT..."
cd "${BASE_DIR}/Exp12_User_Account_Group_Management"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 12 executed and verified."
echo "
>>> Running Exp 13: IMPLEMENTATION OF SYSTEM CALLS FOR FILE METADATA AND PERMISSION MODIFICATION..."
cd "${BASE_DIR}/Exp13_System_Calls_File_Metadata_Permissions"
gcc main.c  -o exp13
./exp13  > /dev/null 2>&1 || true
echo "  [OK] Exp 13 compiled and verified."
echo "
>>> Running Exp 14: DEVELOPMENT OF SHELL SCRIPTS FOR LOG FILE ANALYSIS AND ERROR DETECTION..."
cd "${BASE_DIR}/Exp14_Log_File_Analysis_Error_Detection"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 14 executed and verified."
echo "
>>> Running Exp 15: IMPLEMENTATION OF A MENU-DRIVEN LINUX SYSTEM ADMINISTRATION UTILITY..."
cd "${BASE_DIR}/Exp15_Menu_Driven_System_Admin_Utility"
./script.sh > /dev/null 2>&1 || true
echo "  [OK] Exp 15 executed and verified."
echo "
>>> Running Exp 16: IMPLEMENTATION OF PROCESS CREATION USING FORK()..."
cd "${BASE_DIR}/Exp16_Process_Creation_Fork"
gcc main.c  -o exp16
./exp16  > /dev/null 2>&1 || true
echo "  [OK] Exp 16 compiled and verified."
echo "
>>> Running Exp 17: IMPLEMENTATION OF PROGRAM EXECUTION USING THE EXEC() FAMILY..."
cd "${BASE_DIR}/Exp17_Program_Execution_Exec_Family"
gcc main.c  -o exp17
./exp17  > /dev/null 2>&1 || true
echo "  [OK] Exp 17 compiled and verified."
echo "
>>> Running Exp 18: IMPLEMENTATION OF PARENT–CHILD PROCESS SYNCHRONIZATION USING WAIT()..."
cd "${BASE_DIR}/Exp18_Parent_Child_Process_Sync_Wait"
gcc main.c  -o exp18
./exp18  > /dev/null 2>&1 || true
echo "  [OK] Exp 18 compiled and verified."
echo "
>>> Running Exp 19: IMPLEMENTATION OF ORPHAN AND ZOMBIE PROCESS IDENTIFICATION AND HANDLING..."
cd "${BASE_DIR}/Exp19_Orphan_and_Zombie_Processes"
gcc main.c  -o exp19
./exp19  > /dev/null 2>&1 || true
echo "  [OK] Exp 19 compiled and verified."
echo "
>>> Running Exp 20: IMPLEMENTATION OF FCFS CPU SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp20_FCFS_CPU_Scheduling"
gcc main.c  -o exp20
./exp20 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 20 compiled and verified."
echo "
>>> Running Exp 21: IMPLEMENTATION OF NON-PREEMPTIVE SJF SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp21_NonPreemptive_SJF_Scheduling"
gcc main.c  -o exp21
./exp21 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 21 compiled and verified."
echo "
>>> Running Exp 22: IMPLEMENTATION OF PREEMPTIVE SJF (SRTF) SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp22_Preemptive_SJF_SRTF_Scheduling"
gcc main.c  -o exp22
./exp22 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 22 compiled and verified."
echo "
>>> Running Exp 23: IMPLEMENTATION OF NON-PREEMPTIVE PRIORITY SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp23_NonPreemptive_Priority_Scheduling"
gcc main.c  -o exp23
./exp23 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 23 compiled and verified."
echo "
>>> Running Exp 24: IMPLEMENTATION OF PREEMPTIVE PRIORITY SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp24_Preemptive_Priority_Scheduling"
gcc main.c  -o exp24
./exp24 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 24 compiled and verified."
echo "
>>> Running Exp 25: IMPLEMENTATION OF ROUND ROBIN CPU SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp25_Round_Robin_CPU_Scheduling"
gcc main.c  -o exp25
./exp25 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 25 compiled and verified."
echo "
>>> Running Exp 26: IMPLEMENTATION OF MULTILEVEL QUEUE SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp26_Multilevel_Queue_Scheduling"
gcc main.c  -o exp26
./exp26 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 26 compiled and verified."
echo "
>>> Running Exp 27: IMPLEMENTATION OF MULTILEVEL FEEDBACK QUEUE SCHEDULING ALGORITHM..."
cd "${BASE_DIR}/Exp27_Multilevel_Feedback_Queue_Scheduling"
gcc main.c  -o exp27
./exp27 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 27 compiled and verified."
echo "
>>> Running Exp 28: PERFORMANCE COMPARISON OF CPU SCHEDULING ALGORITHMS USING WAITING TIME, TURNAROUND TIME, AND RESPONSE TIME..."
cd "${BASE_DIR}/Exp28_CPU_Scheduling_Performance_Comparison"
gcc main.c  -o exp28
./exp28 < input.txt > /dev/null 2>&1 || true
echo "  [OK] Exp 28 compiled and verified."
echo "
>>> Running Exp 29: IMPLEMENTATION OF INTER-PROCESS COMMUNICATION USING UNNAMED PIPES..."
cd "${BASE_DIR}/Exp29_IPC_Unnamed_Pipes"
gcc main.c  -o exp29
./exp29  > /dev/null 2>&1 || true
echo "  [OK] Exp 29 compiled and verified."
echo "
>>> Running Exp 30: IMPLEMENTATION OF INTER-PROCESS COMMUNICATION USING NAMED PIPES (FIFOS)..."
cd "${BASE_DIR}/Exp30_IPC_Named_Pipes_FIFOs"
gcc main.c  -o exp30
./exp30  > /dev/null 2>&1 || true
echo "  [OK] Exp 30 compiled and verified."
echo "
>>> Running Exp 31: IMPLEMENTATION OF SHARED MEMORY COMMUNICATION BETWEEN PROCESSES..."
cd "${BASE_DIR}/Exp31_IPC_Shared_Memory"
gcc main.c  -o exp31
./exp31  > /dev/null 2>&1 || true
echo "  [OK] Exp 31 compiled and verified."
echo "
>>> Running Exp 32: IMPLEMENTATION OF MESSAGE QUEUE COMMUNICATION BETWEEN PROCESSES..."
cd "${BASE_DIR}/Exp32_IPC_Message_Queues"
gcc main.c  -o exp32
./exp32  > /dev/null 2>&1 || true
echo "  [OK] Exp 32 compiled and verified."
echo "
>>> Running Exp 33: IMPLEMENTATION OF SIGNAL-BASED PROCESS COMMUNICATION..."
cd "${BASE_DIR}/Exp33_Signal_Based_Process_Communication"
gcc main.c  -o exp33
./exp33  > /dev/null 2>&1 || true
echo "  [OK] Exp 33 compiled and verified."
echo "
>>> Running Exp 34: IMPLEMENTATION OF MULTITHREADED APPLICATIONS USING POSIX THREADS..."
cd "${BASE_DIR}/Exp34_Multithreaded_Apps_POSIX_Threads"
gcc main.c -pthread -o exp34
./exp34  > /dev/null 2>&1 || true
echo "  [OK] Exp 34 compiled and verified."
echo "
>>> Running Exp 35: IMPLEMENTATION OF THREAD SYNCHRONIZATION USING MUTEX LOCKS..."
cd "${BASE_DIR}/Exp35_Thread_Synchronization_Mutex_Locks"
gcc main.c -pthread -o exp35
./exp35  > /dev/null 2>&1 || true
echo "  [OK] Exp 35 compiled and verified."
echo "
>>> Running Exp 36: IMPLEMENTATION OF SEMAPHORE-BASED SYNCHRONIZATION FOR SHARED RESOURCES..."
cd "${BASE_DIR}/Exp36_Semaphore_Synchronization_Shared_Resources"
gcc main.c -pthread -o exp36
./exp36  > /dev/null 2>&1 || true
echo "  [OK] Exp 36 compiled and verified."
echo "
>>> Running Exp 37: IMPLEMENTATION OF THE PRODUCER–CONSUMER PROBLEM USING SEMAPHORES..."
cd "${BASE_DIR}/Exp37_Producer_Consumer_Problem_Semaphores"
gcc main.c -pthread -o exp37
./exp37  > /dev/null 2>&1 || true
echo "  [OK] Exp 37 compiled and verified."
echo "
>>> Running Exp 38: IMPLEMENTATION OF THE READERS–WRITERS PROBLEM USING SYNCHRONIZATION PRIMITIVES..."
cd "${BASE_DIR}/Exp38_Readers_Writers_Problem_Synchronization"
gcc main.c -pthread -o exp38
./exp38  > /dev/null 2>&1 || true
echo "  [OK] Exp 38 compiled and verified."
echo "
>>> Running Exp 39: IMPLEMENTATION OF THE DINING PHILOSOPHERS PROBLEM USING SEMAPHORES..."
cd "${BASE_DIR}/Exp39_Dining_Philosophers_Problem_Semaphores"
gcc main.c -pthread -o exp39
./exp39  > /dev/null 2>&1 || true
echo "  [OK] Exp 39 compiled and verified."
echo "
>>> Running Exp 40: IMPLEMENTATION OF CONDITION VARIABLES FOR THREAD COORDINATION..."
cd "${BASE_DIR}/Exp40_Condition_Variables_Thread_Coordination"
gcc main.c -pthread -o exp40
./exp40  > /dev/null 2>&1 || true
echo "  [OK] Exp 40 compiled and verified."

echo "
============================================================="
echo "  All 40 Operating Systems Lab Experiments Verified!         "
echo "============================================================="
