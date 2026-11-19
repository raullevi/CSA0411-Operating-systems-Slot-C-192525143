CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -pthread -O2

TARGET = measure_bench

all: $(TARGET)

$(TARGET): measure_bench.c
	$(CC) $(CFLAGS) -o $(TARGET) measure_bench.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all run clean
