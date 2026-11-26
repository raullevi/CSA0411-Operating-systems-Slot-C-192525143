#include <stdio.h> 
#include <pthread.h> 
  
#define N 12 
#define T 3 
int a[N] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}; 
int partial[T]; 
  
void *sum_part(void *arg) 
{ 
    int id = *(int *)arg, i; 
    int start = id * (N / T), end = start + N / T; 
    partial[id] = 0; 
    for (i = start; i < end; i++) 
        partial[id] += a[i]; 
    printf("Thread %d: sum of a[%d..%d] = %d\n", id, start, end - 1, partial[id]); 
    return NULL; 
} 
  
int main() 
{ 
    pthread_t th[T]; 
    int id[T], i, total = 0; 
  
    for (i = 0; i < T; i++) { 
        id[i] = i; 
        pthread_create(&th[i], NULL, sum_part, &id[i]); 
    } 
    for (i = 0; i < T; i++) 
        pthread_join(th[i], NULL); 
    for (i = 0; i < T; i++) 
        total += partial[i]; 
    printf("Total sum = %d\n", total); 
    return 0; 
}
