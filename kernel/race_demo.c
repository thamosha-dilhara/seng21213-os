#include "process.h"
#include "mutex.h"
#include "vga.h"

#define RACE_ITERATIONS 50000

static volatile uint32_t unsafe_global = 0;
static volatile uint32_t safe_global   = 0;
static mutex_t race_mutex;

static volatile int race_done_a = 0;
static volatile int race_done_b = 0;
static volatile int use_mutex_mode = 0;

static void racer_a(void) {
    for (uint32_t i = 0; i < RACE_ITERATIONS; i++) {
        if (use_mutex_mode) {
            mutex_lock(&race_mutex);
            safe_global = safe_global + 1;
            mutex_unlock(&race_mutex);
        } else {
            uint32_t tmp = unsafe_global;
            for (volatile int d = 0; d < 50; d++);  /* widen the race window */
            tmp = tmp + 1;
            unsafe_global = tmp;
        }
    }
    race_done_a = 1;
    while (1);
}

static void racer_b(void) {
    for (uint32_t i = 0; i < RACE_ITERATIONS; i++) {
        if (use_mutex_mode) {
            mutex_lock(&race_mutex);
            safe_global = safe_global + 1;
            mutex_unlock(&race_mutex);
        } else {
            uint32_t tmp = unsafe_global;
            for (volatile int d = 0; d < 50; d++);  /* widen the race window */
            tmp = tmp + 1;
            unsafe_global = tmp;
        }
    }
    race_done_b = 1;
    while (1);
}

void race_demo_reset(int with_mutex) {
    unsafe_global = 0;
    safe_global = 0;
    use_mutex_mode = with_mutex;
    race_done_a = 0;
    race_done_b = 0;
    mutex_init(&race_mutex);
}

void *race_demo_a_fn(void) { return (void *)racer_a; }
void *race_demo_b_fn(void) { return (void *)racer_b; }
int   race_demo_finished(void) { return race_done_a && race_done_b; }
uint32_t race_demo_value(void) { return use_mutex_mode ? safe_global : unsafe_global; }
uint32_t race_demo_expected(void) { return RACE_ITERATIONS * 2; }
