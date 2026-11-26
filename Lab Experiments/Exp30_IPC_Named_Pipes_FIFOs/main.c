#include <stdio.h> 
#include <string.h> 
#include <fcntl.h> 
#include <unistd.h> 
#include <sys/stat.h> 
#include <sys/wait.h> 
  
int main() 
{ 
    char *fifo = "myfifo"; 
    char buf[100]; 
  
    mkfifo(fifo, 0666); 
    printf("Named pipe '%s' created\n", fifo); 
    fflush(stdout); 
  
    if (fork() == 0) {               /* reader */ 
        int fd = open(fifo, O_RDONLY); 
        int n = read(fd, buf, sizeof(buf) - 1); 
        buf[n] = '\0'; 
        printf("Reader received: %s\n", buf); 
        close(fd); 
        return 0; 
    } 
    int fd = open(fifo, O_WRONLY);     /* writer */ 
    char msg[] = "Data sent through FIFO"; 
    printf("Writer sending : %s\n", msg); 
    fflush(stdout); 
    write(fd, msg, strlen(msg)); 
    close(fd); 
    wait(NULL); 
    unlink(fifo); 
    printf("FIFO removed\n"); 
    return 0; 
}
