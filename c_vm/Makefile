# Compiler settings
CC = gcc
CFLAGS = -Wall -g

# Target executable name (Windows uses .exe)
TARGET = main.exe

# Build the executable
$(TARGET): main.o
	$(CC) $(CFLAGS) -o $(TARGET) main.o

# Compile source files into object files
main.o: main.c main.h
	$(CC) $(CFLAGS) -c main.c

# Clean up build files (Windows command)
clean:
	del $(TARGET) *.o