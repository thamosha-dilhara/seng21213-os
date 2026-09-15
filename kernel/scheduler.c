#include "scheduler.h"
#include "process.h"

extern void switch_context(uint32_t *old_esp_store, uint32_t new_esp);

static int ready_queue[MAX_PROCESSES];
static int ready_count = 0;
static int current_virtual = 0;
static uint32_t kernel_esp = 0;
static int scheduler_running = 0;

void scheduler_init(void) {
    ready_count = 0;
    current_virtual = 0;
    scheduler_running = 0;
}

void scheduler_add(int slot) {
    if (ready_count < MAX_PROCESSES) {
        ready_queue[ready_count++] = slot;
    }
}

void scheduler_start(void) {
    current_virtual = ready_count;
    scheduler_running = 1;
}

void scheduler_tick(void) {
    if (!scheduler_running || ready_count == 0) return;

    int total = ready_count + 1;
    int prev_virtual = current_virtual;
    current_virtual = (current_virtual + 1) % total;

    if (prev_virtual == current_virtual) return;

    uint32_t *prev_esp_ptr;
    uint32_t  next_esp_val;

    if (prev_virtual == ready_count) {
        prev_esp_ptr = &kernel_esp;
    } else {
        pcb_t *p = process_table_get(ready_queue[prev_virtual]);
        p->state = PROC_READY;
        prev_esp_ptr = &p->esp;
    }

    if (current_virtual == ready_count) {
        next_esp_val = kernel_esp;
    } else {
        pcb_t *p = process_table_get(ready_queue[current_virtual]);
        p->state = PROC_RUNNING;
        next_esp_val = p->esp;
    }

    switch_context(prev_esp_ptr, next_esp_val);
}
