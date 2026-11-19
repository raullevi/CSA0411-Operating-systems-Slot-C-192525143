CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

TARGET = copy_file_todo

all: $(TARGET)

$(TARGET): copy_file_todo.c
	$(CC) $(CFLAGS) -o $(TARGET) copy_file_todo.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o records.dat copy.dat

.PHONY: all run clean
