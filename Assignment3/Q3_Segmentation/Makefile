CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

all: segmentation_sim

segmentation_sim: segmentation_sim.c
	$(CC) $(CFLAGS) segmentation_sim.c -o segmentation_sim

clean:
	rm -f segmentation_sim *.o
