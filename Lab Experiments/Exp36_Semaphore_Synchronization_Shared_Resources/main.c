#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 
  
sem_t printers; 
  
void *user(void *arg) 
{ 
    int id = *(int *)arg; 
    printf("User %d waiting for a printer\n", id); 
    sem_wait(&printers); 
    printf("User %d is PRINTING\n", id); 
    usleep(300000); 
    printf("User %d finished printing\n", id); 
    sem_post(&printers); 
    return NULL; 
} 
  
int main() 
{ 
    pthread_t t[5]; 
    int id[5], i; 
    sem_init(&printers, 0, 2); 
    for (i = 0; i < 5; i++) { 
        id[i] = i + 1; 
        pthread_create(&t[i], NULL, user, &id[i]); 
        usleep(50000); 
    } 
    for (i = 0; i < 5; i++) 
        pthread_join(t[i], NULL); 
    sem_destroy(&printers); 
    printf("All users served using 2 printers\n"); 
    return 0; 
}
