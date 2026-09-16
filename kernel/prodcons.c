#include "prodcons.h"
#include "semaphore.h"
#include "mutex.h"

#define BUFFER_SIZE 5
#define TOTAL_ITEMS 20

static int buffer[BUFFER_SIZE];
static int buf_in = 0;
static int buf_out = 0;

static semaphore_t sem_empty;
static semaphore_t sem_full;
static mutex_t      buf_mutex;

static volatile uint32_t produced_count = 0;
static volatile uint32_t consumed_count = 0;
static volatile int producer_done = 0;
static volatile int consumer_done = 0;
static volatile int corruption = 0;
static volatile int next_expected = 0;

void prodcons_reset(void) {
    buf_in = 0;
    buf_out = 0;
    produced_count = 0;
    consumed_count = 0;
    producer_done = 0;
    consumer_done = 0;
    corruption = 0;
    next_expected = 0;
    sem_init(&sem_empty, BUFFER_SIZE);
    sem_init(&sem_full, 0);
    mutex_init(&buf_mutex);
}

static void producer(void) {
    for (int i = 0; i < TOTAL_ITEMS; i++) {
        sem_wait(&sem_empty);
        mutex_lock(&buf_mutex);

        buffer[buf_in] = i;
        buf_in = (buf_in + 1) % BUFFER_SIZE;
        produced_count++;

        mutex_unlock(&buf_mutex);
        sem_signal(&sem_full);
    }
    producer_done = 1;
    while (1);
}

static void consumer(void) {
    for (int i = 0; i < TOTAL_ITEMS; i++) {
        sem_wait(&sem_full);
        mutex_lock(&buf_mutex);

        int item = buffer[buf_out];
        buf_out = (buf_out + 1) % BUFFER_SIZE;
        consumed_count++;

        if (item != next_expected) {
            corruption = 1;
        }
        next_expected++;

        mutex_unlock(&buf_mutex);
        sem_signal(&sem_empty);
    }
    consumer_done = 1;
    while (1);
}

void     *prodcons_producer_fn(void) { return (void *)producer; }
void     *prodcons_consumer_fn(void) { return (void *)consumer; }
int       prodcons_finished(void) { return producer_done && consumer_done; }
int       prodcons_corruption_detected(void) { return corruption; }
uint32_t  prodcons_items_produced(void) { return produced_count; }
uint32_t  prodcons_items_consumed(void) { return consumed_count; }
int       prodcons_debug_empty(void) { return sem_empty.count; }
int       prodcons_debug_full(void) { return sem_full.count; }
int       prodcons_debug_mutex_locked(void) { return buf_mutex.locked; }
int       prodcons_debug_producer_done(void) { return producer_done; }
int       prodcons_debug_consumer_done(void) { return consumer_done; }
