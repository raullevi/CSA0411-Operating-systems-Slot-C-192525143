#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 
  
#define SIZE 5 
#define ITEMS 8 
int buffer[SIZE], in = 0, out = 0; 
sem_t empty, full; 
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER; 
  
void *producer(void *arg) 
{ 
    for (int item = 1; item <= ITEMS; item++) { 
        sem_wait(&empty); 
        pthread_mutex_lock(&mutex); 
        buffer[in] = item; 
        printf("Producer produced item %d at position %d\n", item, in); 
        in = (in + 1) % SIZE; 
        pthread_mutex_unlock(&mutex); 
        sem_post(&full); 
        usleep(100000); 
    } 
    return NULL; 
} 
  
void *consumer(void *arg) 
{ 
    for (int i = 1; i <= ITEMS; i++) { 
        sem_wait(&full); 
        pthread_mutex_lock(&mutex); 
        int item = buffer[out]; 
        printf("Consumer consumed item %d from position %d\n", item, out); 
        out = (out + 1) % SIZE; 
        pthread_mutex_unlock(&mutex); 
        sem_post(&empty); 
        usleep(250000); 
    } 
    return NULL; 
} 
  
int main() 
{ 
    pthread_t p, c; 
    sem_init(&empty, 0, SIZE); 
    sem_init(&full, 0, 0); 
    pthread_create(&p, NULL, producer, NULL); 
    pthread_create(&c, NULL, consumer, NULL); 
    pthread_join(p, NULL); 
    pthread_join(c, NULL); 
    printf("All %d items produced and consumed\n", ITEMS); 
    return 0; 
}
