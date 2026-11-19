CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

TARGETS = disk_sched_todo disk_sim_suite

all: $(TARGETS)

disk_sched_todo: disk_sched_todo.c
	$(CC) $(CFLAGS) -o disk_sched_todo disk_sched_todo.c

disk_sim_suite: disk_sim_suite.c
	$(CC) $(CFLAGS) -o disk_sim_suite disk_sim_suite.c

run: all
	@echo "--- 1. Running Completed Code (Matching PDF Specification) ---"
	./disk_sched_todo
	@echo "\n--- 2. Running Extended Simulation & Starvation Suite ---"
	./disk_sim_suite

clean:
	rm -f $(TARGETS) *.o

.PHONY: all run clean
