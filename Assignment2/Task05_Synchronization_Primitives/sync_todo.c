#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#ifdef __APPLE__
/* macOS Darwin stubs sem_init with ENOSYS; provide transparent POSIX semaphore wrapper */
typedef struct {
    pthread_mutex_t m;
    pthread_cond_t c;
    int v;
} mac_sem_t;

static inline int mac_sem_init(mac_sem_t *s, int pshared, unsigned int val) {
    (void)pshared;
    pthread_mutex_init(&s->m, NULL);
    pthread_cond_init(&s->c, NULL);
    s->v = (int)val;
    return 0;
}
static inline int mac_sem_wait(mac_sem_t *s) {
    pthread_mutex_lock(&s->m);
    while (s->v <= 0) pthread_cond_wait(&s->c, &s->m);
    s->v--;
    pthread_mutex_unlock(&s->m);
    return 0;
}
static inline int mac_sem_post(mac_sem_t *s) {
    pthread_mutex_lock(&s->m);
    s->v++;
    pthread_cond_signal(&s->c);
    pthread_mutex_unlock(&s->m);
    return 0;
}
static inline int mac_sem_destroy(mac_sem_t *s) {
    pthread_mutex_destroy(&s->m);
    pthread_cond_destroy(&s->c);
    return 0;
}
#define sem_t mac_sem_t
#define sem_init mac_sem_init
#define sem_wait mac_sem_wait
#define sem_post mac_sem_post
#define sem_destroy mac_sem_destroy
#endif

#define SIZE 5
#define ITEMS 20

int buffer[SIZE], in = 0, out = 0;
sem_t empty, full;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
long consumed_sum = 0;

void *producer(void *arg)
{
    (void)arg;
    for (int item = 1; item <= ITEMS; item++) {
        // TODO 1: Wait on empty, lock the mutex, put item at buffer[in], advance in
        //         circularly, unlock, then post full
        sem_wait(&empty);
        pthread_mutex_lock(&lock);
        buffer[in] = item;
        in = (in + 1) % SIZE;
        pthread_mutex_unlock(&lock);
        sem_post(&full);
    }
    return NULL;
}

void *consumer(void *arg)
{
    (void)arg;
    for (int k = 0; k < ITEMS; k++) {
        // TODO 2: Wait on full, lock the mutex, take the item at buffer[out], advance
        //         out circularly, unlock, post empty and add the item to consumed_sum
        sem_wait(&full);
        pthread_mutex_lock(&lock);
        int item = buffer[out];
        out = (out + 1) % SIZE;
        pthread_mutex_unlock(&lock);
        sem_post(&empty);
        consumed_sum += item;
    }
    return NULL;
}

int main(void)
{
    sem_init(&empty, 0, SIZE);
    sem_init(&full, 0, 0);
    pthread_t p, c;
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);
    pthread_join(p, NULL);
    pthread_join(c, NULL);
    printf("items consumed: %d, sum = %ld (expected %d)\n", ITEMS, consumed_sum,
           ITEMS * (ITEMS + 1) / 2);
    sem_destroy(&empty);
    sem_destroy(&full);
    return 0;
}
