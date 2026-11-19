CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -pthread -O2

TARGET = process_tree_sim

all: $(TARGET)

$(TARGET): process_tree_sim.c
	$(CC) $(CFLAGS) -o $(TARGET) process_tree_sim.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all run clean
