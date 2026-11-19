CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

all: paging_todo paging_sim

paging_todo: paging_todo.c
	$(CC) $(CFLAGS) paging_todo.c -o paging_todo

paging_sim: paging_sim.c
	$(CC) $(CFLAGS) paging_sim.c -o paging_sim

clean:
	rm -f paging_todo paging_sim *.o
