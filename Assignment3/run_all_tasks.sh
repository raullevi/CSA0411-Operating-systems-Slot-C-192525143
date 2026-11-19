#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo "=========================================================================="
echo "  SIMATS ENGINEERING - DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
echo "  CSA0411 OPERATING SYSTEMS (SLOT C) - ASSIGNMENT 3 (CO3)"
echo "  Student Name   : Rakul K"
echo "  Register Number: 192525143"
echo "  Date & Time    : $(date)"
echo "=========================================================================="

echo -e "\n>>> EXECUTING TASK 1: LINKING, LOADING & ADDRESS BINDING..."
cd "$REPO_DIR/Q1_Linking_Loading"
./run_q1_experiments.sh

echo -e "\n>>> EXECUTING TASK 2: PAGING..."
cd "$REPO_DIR/Q2_Paging"
./run_q2_experiments.sh

echo -e "\n>>> EXECUTING TASK 3: SEGMENTATION..."
cd "$REPO_DIR/Q3_Segmentation"
./run_q3_experiments.sh

echo -e "\n>>> EXECUTING TASK 4: VIRTUAL MEMORY & DEMAND PAGING..."
cd "$REPO_DIR/Q4_Virtual_Memory"
./run_q4_experiments.sh

echo -e "\n>>> EXECUTING TASK 5: PAGE-REPLACEMENT TECHNIQUES..."
cd "$REPO_DIR/Q5_Page_Replacement"
./run_q5_experiments.sh

echo -e "\n>>> EXECUTING TASK 6: DISK MANAGEMENT..."
cd "$REPO_DIR/Q6_Disk_Management"
./run_q6_experiments.sh

echo -e "\n>>> EXECUTING TASK 7: MEMORY MANAGEMENT PLAN FROM FIRST PRINCIPLES..."
cd "$REPO_DIR/Q7_Memory_Management_Plan"
./run_q7_experiments.sh

cd "$REPO_DIR"
echo -e "\n=========================================================================="
echo "  ALL 7 ASSIGNMENT TASKS EXECUTED AND VERIFIED SUCCESSFULLY!"
echo "=========================================================================="
