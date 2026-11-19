#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

LOG="experiment_q1_results.log"
exec > >(tee "$LOG") 2>&1

echo "=========================================================================="
echo "  CSA0411 OS ASSIGNMENT 3 - QUESTION 1 EXPERIMENTAL INVESTIGATION LOG"
echo "  Student: Rakul K | Register Number: 192525143"
echo "  Date: $(date)"
echo "=========================================================================="

echo -e "\n[STEP 1] Cleaning and Building All Artifacts..."
make clean
make

echo -e "\n[STEP 2] Comparing Executable & Library File Sizes:"
ls -lh bank_app_static bank_app_dynamic bank_app_dlopen libencrypt.a libencrypt.dylib libencrypt_v1.dylib libencrypt_v2.dylib 2>/dev/null || ls -lh bank_app_static bank_app_dynamic bank_app_dlopen libencrypt.a libencrypt.so libencrypt_v1.so libencrypt_v2.so

echo -e "\n[STEP 3] Inspecting Dynamic Dependencies (ldd / otool -L):"
if command -v ldd >/dev/null 2>&1; then
    echo "--- Static Executable (ldd) ---"
    ldd bank_app_static || true
    echo "--- Dynamic Executable (ldd) ---"
    ldd bank_app_dynamic || true
    echo "--- dlopen Executable (ldd) ---"
    ldd bank_app_dlopen || true
else
    echo "--- Static Executable (otool -L) ---"
    otool -L bank_app_static || true
    echo "--- Dynamic Executable (otool -L) ---"
    otool -L bank_app_dynamic || true
    echo "--- dlopen Executable (otool -L) ---"
    otool -L bank_app_dlopen || true
fi

echo -e "\n[STEP 4] Executing Static vs Dynamic Application with v1.0 (Vulnerable):"
cp libencrypt_v1.dylib libencrypt.dylib 2>/dev/null || cp libencrypt_v1.so libencrypt.so
echo ">>> Running bank_app_static:"
./bank_app_static
echo -e "\n>>> Running bank_app_dynamic:"
./bank_app_dynamic

echo -e "\n[STEP 5] Benchmarking Startup Time and Memory Use (Static vs Dynamic):"
echo ">>> Timing bank_app_static (100 iterations loop):"
time for i in $(seq 1 100); do ./bank_app_static >/dev/null; done
echo ">>> Timing bank_app_dynamic (100 iterations loop):"
time for i in $(seq 1 100); do ./bank_app_dynamic >/dev/null; done

echo -e "\n[STEP 6] Hot Library Replacement (Zero-Recompile Security Patch):"
echo "--- Initial dynamic app state before patch ---"
./bank_app_dynamic | grep -E "Active Security|Security Patch"
echo "--- Deploying Security Fix: Replacing libencrypt with v2.1 ---"
cp libencrypt_v2.dylib libencrypt.dylib 2>/dev/null || cp libencrypt_v2.so libencrypt.so
echo "--- Re-running bank_app_dynamic WITHOUT recompiling ---"
./bank_app_dynamic | grep -E "Active Security|Security Patch"
echo "--- Verification: bank_app_static is STILL running vulnerable code unless 200MB rebuilt ---"
./bank_app_static | grep -E "Active Security|Security Patch"

echo -e "\n[STEP 7] Runtime Dynamic Loading with dlopen() and dlsym():"
SO_FILE="./libencrypt.dylib"
[ ! -f "$SO_FILE" ] && SO_FILE="./libencrypt.so"
./bank_app_dlopen "$SO_FILE"

echo -e "\n[STEP 8] Missing Shared Library Failure Testing:"
echo "--- Renaming shared library to simulate missing file ---"
mv libencrypt.dylib libencrypt.dylib.missing 2>/dev/null || mv libencrypt.so libencrypt.so.missing
echo ">>> (A) Testing dynamic application failure behavior:"
./bank_app_dynamic || echo "-> Dynamic app terminated by dynamic linker (fatal crash at load time)."
echo -e "\n>>> (B) Testing dlopen application failure behavior:"
./bank_app_dlopen "$SO_FILE" || echo "-> dlopen app caught failure gracefully at runtime."
mv libencrypt.dylib.missing libencrypt.dylib 2>/dev/null || mv libencrypt.so.missing libencrypt.so

echo -e "\n[STEP 9] Concurrent Multi-Instance Execution & Shared Code Pages:"
echo "Launching two background instances of bank_app_dynamic..."
./bank_app_dynamic --pause > instance1.log 2>&1 &
PID1=$!
./bank_app_dynamic --pause > instance2.log 2>&1 &
PID2=$!
sleep 2

echo "Both instances active: PID1=$PID1, PID2=$PID2"
if command -v vmmap >/dev/null 2>&1; then
    echo "Examining shared library region in PID $PID1:"
    vmmap -summary $PID1 | grep -E "REGION TYPE|TOTAL|__TEXT" || true
elif [ -f "/proc/$PID1/smaps" ]; then
    echo "Linux smaps shared pages for PID $PID1:"
    grep -A 8 "libencrypt" "/proc/$PID1/smaps" || true
else
    ps -o pid,ppid,rss,vsz,comm -p $PID1,$PID2
fi

wait $PID1 $PID2
rm -f instance1.log instance2.log

echo -e "\n=========================================================================="
echo "  QUESTION 1 EXPERIMENTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
