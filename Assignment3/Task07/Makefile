CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

all: rt_memory_lock_benchmark edge_device_memory_sim

rt_memory_lock_benchmark: rt_memory_lock_benchmark.c
	$(CC) $(CFLAGS) rt_memory_lock_benchmark.c -o rt_memory_lock_benchmark

edge_device_memory_sim: edge_device_memory_sim.c
	$(CC) $(CFLAGS) edge_device_memory_sim.c -o edge_device_memory_sim

clean:
	rm -f rt_memory_lock_benchmark edge_device_memory_sim *.o
