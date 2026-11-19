CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -pthread -O2

TARGETS = pipe_ipc_todo ipc_comparison_bench

all: $(TARGETS)

pipe_ipc_todo: pipe_ipc_todo.c
	$(CC) $(CFLAGS) -o pipe_ipc_todo pipe_ipc_todo.c

ipc_comparison_bench: ipc_comparison_bench.c
	$(CC) $(CFLAGS) -o ipc_comparison_bench ipc_comparison_bench.c

run: all
	@echo "--- 1. Running Completed Pipe IPC Code (Matching PDF Specification) ---"
	./pipe_ipc_todo
	@echo "\n--- 2. Running IPC Throughput Benchmark (Pipe vs Shared Memory) ---"
	./ipc_comparison_bench

clean:
	rm -f $(TARGETS) *.o

.PHONY: all run clean
