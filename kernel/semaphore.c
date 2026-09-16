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
        __asm__ __volatile__("hlt");
        /* hlt pauses the CPU until the next interrupt (the timer),
         * guaranteeing the scheduler gets a chance to run other tasks
         * instead of racing to re-lock cli before the tick can land. */
    }
}

void sem_signal(semaphore_t *s) {
    __asm__ __volatile__("cli");
    s->count++;
    __asm__ __volatile__("sti");
}
