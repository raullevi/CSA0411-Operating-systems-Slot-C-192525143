CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

TARGETS = bankers_todo bankers_scale_bench

all: $(TARGETS)

bankers_todo: bankers_todo.c
	$(CC) $(CFLAGS) -o bankers_todo bankers_todo.c

bankers_scale_bench: bankers_scale_bench.c
	$(CC) $(CFLAGS) -o bankers_scale_bench bankers_scale_bench.c

run: all
	@echo "--- 1. Running Completed Banker's Algorithm (Matching PDF Specification) ---"
	./bankers_todo
	@echo "\n--- 2. Running Banker's Scalability Benchmark (N=10, 100, 1000) ---"
	./bankers_scale_bench

clean:
	rm -f $(TARGETS) *.o

.PHONY: all run clean
