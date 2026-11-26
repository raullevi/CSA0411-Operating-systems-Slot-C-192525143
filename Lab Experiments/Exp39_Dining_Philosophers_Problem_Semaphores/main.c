#include <stdio.h> 
#include <pthread.h> 
#include <semaphore.h> 
#include <unistd.h> 
  
#define N 5 
sem_t chopstick[N]; 
  
void *philosopher(void *arg) 
{ 
    int id = *(int *)arg; 
    int left = id, right = (id + 1) % N; 
    int first = (id % 2 == 0) ? left : right; 
    int second = (id % 2 == 0) ? right : left; 
  
    for (int meal = 1; meal <= 2; meal++) { 
        printf("Philosopher %d is thinking\n", id); 
        usleep(100000); 
        sem_wait(&chopstick[first]); 
        sem_wait(&chopstick[second]); 
        printf("Philosopher %d is eating (meal %d) with chopsticks %d and %d\n", id, 
meal, left, right); 
        usleep(150000); 
        sem_post(&chopstick[second]); 
        sem_post(&chopstick[first]); 
        printf("Philosopher %d finished eating\n", id); 
    } 
    return NULL; 
} 
  
int main() 
{ 
    pthread_t t[N]; 
    int id[N], i; 
    for (i = 0; i < N; i++) 
        sem_init(&chopstick[i], 0, 1); 
    for (i = 0; i < N; i++) { 
        id[i] = i; 
        pthread_create(&t[i], NULL, philosopher, &id[i]); 
    } 
    for (i = 0; i < N; i++) 
        pthread_join(t[i], NULL); 
    printf("All philosophers have eaten. No deadlock.\n"); 
    return 0; 
}
