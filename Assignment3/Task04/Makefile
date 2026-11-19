CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

all: vm_experiments

vm_experiments: vm_experiments.c
	$(CC) $(CFLAGS) vm_experiments.c -o vm_experiments

clean:
	rm -f vm_experiments *.o *.csv *.svg
