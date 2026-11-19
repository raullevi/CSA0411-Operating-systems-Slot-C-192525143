CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

TARGET = file_alloc_todo

all: $(TARGET)

$(TARGET): file_alloc_todo.c
	$(CC) $(CFLAGS) -o $(TARGET) file_alloc_todo.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all run clean
