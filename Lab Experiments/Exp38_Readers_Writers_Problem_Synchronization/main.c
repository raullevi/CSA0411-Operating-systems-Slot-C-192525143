#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 
  
int data = 0, read_count = 0; 
sem_t wrt; 
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER; 
  
void *reader(void *arg) 
{ 
    int id = *(int *)arg; 
    pthread_mutex_lock(&mutex); 
    read_count++; 
    if (read_count == 1) sem_wait(&wrt); 
    pthread_mutex_unlock(&mutex); 
  
    printf("Reader %d reads data = %d (readers inside = %d)\n", id, data, read_count); 
    usleep(200000); 
  
    pthread_mutex_lock(&mutex); 
    read_count--; 
    if (read_count == 0) sem_post(&wrt); 
    pthread_mutex_unlock(&mutex); 
    return NULL; 
} 
  
void *writer(void *arg) 
{ 
    int id = *(int *)arg; 
    sem_wait(&wrt); 
    data += 10; 
    printf("Writer %d writes data = %d\n", id, data); 
    usleep(200000); 
    sem_post(&wrt); 
    return NULL; 
} 
  
int main() 
{ 
    pthread_t r[3], w[2]; 
    int rid[3] = {1, 2, 3}, wid[2] = {1, 2}, i; 
    sem_init(&wrt, 0, 1); 
  
    pthread_create(&w[0], NULL, writer, &wid[0]); 
    usleep(50000); 
    for (i = 0; i < 3; i++) 
        pthread_create(&r[i], NULL, reader, &rid[i]); 
    usleep(50000); 
    pthread_create(&w[1], NULL, writer, &wid[1]); 
  
    for (i = 0; i < 3; i++) pthread_join(r[i], NULL); 
    for (i = 0; i < 2; i++) pthread_join(w[i], NULL); 
    printf("Final data = %d\n", data); 
    return 0; 
}
