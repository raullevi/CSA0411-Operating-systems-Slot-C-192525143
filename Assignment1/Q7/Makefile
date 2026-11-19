CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

TARGET = shell_todo

all: $(TARGET)

$(TARGET): shell_todo.c
	$(CC) $(CFLAGS) -o $(TARGET) shell_todo.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all run clean
