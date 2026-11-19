CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

TARGETS = cpu_scheduling_todo cpu_scheduler_suite

all: $(TARGETS)

cpu_scheduling_todo: cpu_scheduling_todo.c
	$(CC) $(CFLAGS) -o cpu_scheduling_todo cpu_scheduling_todo.c

cpu_scheduler_suite: cpu_scheduler_suite.c
	$(CC) $(CFLAGS) -o cpu_scheduler_suite cpu_scheduler_suite.c

run: all
	@echo "--- 1. Running Completed Code (Matching PDF Specification) ---"
	./cpu_scheduling_todo
	@echo "\n--- 2. Running Full Scheduling Suite (Gantt, Metrics & Quantum Study) ---"
	./cpu_scheduler_suite

clean:
	rm -f $(TARGETS) *.o

.PHONY: all run clean
