#!/usr/bin/env bash
# Master Execution Script for Assignment 5 (CO5)
# SIMATS Engineering - Operating Systems (Slot C)
# Student: Rakul K (192525143)

set -euo pipefail
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================================================"
echo " SIMATS ENGINEERING - OPERATING SYSTEMS (CSA0411 / CSA04)"
echo " ASSIGNMENT 5: LINUX, CONTAINERS AND VIRTUALISATION FOR EFFICIENT OPERATIONS"
echo " Student: Rakul K | Register Number: 192525143 | Bloom's Level: K5 (Evaluate)"
echo "================================================================================"

echo -e "\n>>> [1/4] Executing Task B1: Linux Server Administration..."
cd "${BASE_DIR}/TaskB1_Linux_Server_Admin" && bash run_b1.sh

echo -e "\n>>> [2/4] Executing Task B2: Containerise the Result Portal..."
cd "${BASE_DIR}/TaskB2_Containerise_Portal" && bash run_b2.sh

echo -e "\n>>> [3/4] Executing Task B3: Deployment Comparison & Kubernetes Manifest..."
cd "${BASE_DIR}/TaskB3_Deployment_Comparison" && bash run_b3.sh

echo -e "\n>>> [4/4] Executing Task B4: Final Engineering Decision & Capacity Sizing..."
cd "${BASE_DIR}/TaskB4_Final_Engineering_Decision" && bash run_b4.sh

echo -e "\n>>> [Screenshots] Generating Terminal Screenshot Images in output_ss/..."
python3 "${BASE_DIR}/generate_terminal_screenshots.py"

echo -e "\n================================================================================"
echo " All Assignment 5 Tasks Executed and Verified Successfully!"
echo "================================================================================"
