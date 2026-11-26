#include <stdio.h> 
#include <pthread.h> 
#include <unistd.h> 
  
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER; 
pthread_cond_t cond = PTHREAD_COND_INITIALIZER; 
int ready = 0, data = 0; 
  
void *worker(void *arg) 
{ 
    int id = *(int *)arg; 
    pthread_mutex_lock(&m); 
    while (ready == 0) { 
        printf("Worker %d waiting for data\n", id); 
        pthread_cond_wait(&cond, &m); 
    } 
    printf("Worker %d woke up and processed data = %d\n", id, data * id); 
    pthread_mutex_unlock(&m); 
    return NULL; 
} 
  
int main() 
{ 
    pthread_t t[3]; 
    int id[3] = {1, 2, 3}, i; 
    for (i = 0; i < 3; i++) 
        pthread_create(&t[i], NULL, worker, &id[i]); 
    sleep(1); 
  
    pthread_mutex_lock(&m); 
    data = 100; 
    ready = 1; 
    printf("Main thread: data is ready, signalling all workers\n"); 
    pthread_cond_broadcast(&cond); 
    pthread_mutex_unlock(&m); 
  
    for (i = 0; i < 3; i++) 
        pthread_join(t[i], NULL); 
    return 0; 
}
