#include "scheduler.h"
#include "process.h"

extern void switch_context(uint32_t *old_esp_store, uint32_t new_esp);

static int ready_queue[MAX_PROCESSES];
static int ready_count = 0;
static int current_task = -1;   /* -1 = kernel/shell context, always fixed */
static uint32_t kernel_esp = 0;
static int scheduler_running = 0;

void scheduler_init(void) {
    ready_count = 0;
    current_task = -1;
    scheduler_running = 0;
}

void scheduler_add(int slot) {
    if (ready_count < MAX_PROCESSES) {
        ready_queue[ready_count++] = slot;
    }
}

void scheduler_start(void) {
    current_task = -1;
    scheduler_running = 1;
}

void scheduler_tick(void) {
    if (!scheduler_running || ready_count == 0) return;

    int prev_task = current_task;
    int next_task = prev_task + 1;
    if (next_task >= ready_count) {
        next_task = -1;   /* cycle back to kernel/shell */
    }

    if (prev_task == next_task) return;

    uint32_t *prev_esp_ptr;
    uint32_t  next_esp_val;

    if (prev_task == -1) {
        prev_esp_ptr = &kernel_esp;
    } else {
        pcb_t *p = process_table_get(ready_queue[prev_task]);
        p->state = PROC_READY;
        prev_esp_ptr = &p->esp;
    }

    if (next_task == -1) {
        next_esp_val = kernel_esp;
    } else {
        pcb_t *p = process_table_get(ready_queue[next_task]);
        p->state = PROC_RUNNING;
        next_esp_val = p->esp;
    }

    current_task = next_task;
    switch_context(prev_esp_ptr, next_esp_val);
}
