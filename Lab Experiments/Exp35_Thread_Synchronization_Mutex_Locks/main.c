#include <stdio.h> 
#include <pthread.h> 
  
#define LOOPS 1000000 
long counter = 0; 
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER; 
  
void *no_lock(void *arg) 
{ 
    for (int i = 0; i < LOOPS; i++) 
        counter++; 
    return NULL; 
} 
  
void *with_lock(void *arg) 
{ 
    for (int i = 0; i < LOOPS; i++) { 
        pthread_mutex_lock(&lock); 
        counter++; 
        pthread_mutex_unlock(&lock); 
    } 
    return NULL; 
} 
  
void run(void *(*fn)(void *), char *title) 
{ 
    pthread_t t1, t2; 
    counter = 0; 
    pthread_create(&t1, NULL, fn, NULL); 
    pthread_create(&t2, NULL, fn, NULL); 
    pthread_join(t1, NULL); 
    pthread_join(t2, NULL); 
    printf("%-15s: counter = %ld (expected %d)\n", title, counter, 2 * LOOPS); 
} 
  
int main() 
{ 
    run(no_lock, "Without mutex"); 
    run(with_lock, "With mutex"); 
    pthread_mutex_destroy(&lock); 
    return 0; 
}
