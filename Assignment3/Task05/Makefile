CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

all: page_replacement_todo replacement_engine

page_replacement_todo: page_replacement_todo.c
	$(CC) $(CFLAGS) page_replacement_todo.c -o page_replacement_todo

replacement_engine: replacement_engine.c
	$(CC) $(CFLAGS) replacement_engine.c -o replacement_engine

clean:
	rm -f page_replacement_todo replacement_engine *.o *.csv *.svg
