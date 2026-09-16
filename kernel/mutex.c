#include "mutex.h"

void mutex_init(mutex_t *m) {
    m->locked = 0;
}

void mutex_lock(mutex_t *m) {
    while (1) {
        __asm__ __volatile__("cli");
        if (!m->locked) {
            m->locked = 1;
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

void mutex_unlock(mutex_t *m) {
    __asm__ __volatile__("cli");
    m->locked = 0;
    __asm__ __volatile__("sti");
}
