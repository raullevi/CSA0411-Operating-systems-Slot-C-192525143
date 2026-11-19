CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2

TARGET = video_storage_sim

all: $(TARGET)

$(TARGET): video_storage_sim.c
	$(CC) $(CFLAGS) -o $(TARGET) video_storage_sim.c

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: all run clean
