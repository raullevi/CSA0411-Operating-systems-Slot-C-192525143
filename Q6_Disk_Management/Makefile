CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

all: disk_benchmark raid_calculator

disk_benchmark: disk_benchmark.c
	$(CC) $(CFLAGS) disk_benchmark.c -o disk_benchmark

raid_calculator: raid_calculator.c
	$(CC) $(CFLAGS) raid_calculator.c -o raid_calculator

clean:
	rm -f disk_benchmark raid_calculator *.o *.tmp
