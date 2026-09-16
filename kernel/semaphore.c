#include "semaphore.h"

void sem_init(semaphore_t *s, int initial_count) {
    s->count = initial_count;
}

void sem_wait(semaphore_t *s) {
    while (1) {
        __asm__ __volatile__("cli");
        if (s->count > 0) {
            s->count--;
            __asm__ __volatile__("sti");
            return;
        }
        __asm__ __volatile__("sti");
        /* Spin -- timer interrupt still enabled, scheduler keeps running
         * other tasks while this one waits for the count to rise. */
    }
}

void sem_signal(semaphore_t *s) {
    __asm__ __volatile__("cli");
    s->count++;
    __asm__ __volatile__("sti");
}
