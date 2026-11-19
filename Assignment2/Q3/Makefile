CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -pthread -O2

TARGET = camera_threads

all: $(TARGET)

$(TARGET): camera_threads.c
	$(CC) $(CFLAGS) -o $(TARGET) camera_threads.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all run clean
