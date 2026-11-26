# Experiment 35: IMPLEMENTATION OF THREAD SYNCHRONIZATION USING MUTEX LOCKS

**Course Outcome:** CO2  
**Course Code:** CSA04 - Operating Systems  
**Student Name:** Rakul K (192525143)  

## AIM
To write a C program that synchronises threads using mutex locks and shows the race condition 
that occurs without them.

## PROCEDURE
1. Declare a shared counter and a mutex. 
2. Write a thread function that increments the counter 1,000,000 times without locking. 
3. Write a second thread function that locks the mutex before each increment and unlocks 
it after. 
4. Run two threads with the unsynchronised function and display the final counter value. 
5. Reset the counter, run two threads with the mutex -protected function and display the 
result. 
6. Compare the two results with the expected value 2,000,000.

## SOURCE CODE (main.c)
```c
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
```

## EXPECTED & VERIFIED OUTPUT
```
Without mutex  : counter = 1242896 (expected 2000000) 
With mutex     : counter = 2000000 (expected 2000000)
```

## TERMINAL OUTPUT SCREENSHOT

![Exp 35 Terminal Output](exp35_output.png)

## RESULT
Thus thread synchronisation using mutex locks was implemented successfully. Without the 
mutex the counter value was wrong because of the race condition; with the mutex it was correct.
