#include "process.h"
#include "vga.h"

static volatile uint32_t demo_a_count = 0;
static volatile uint32_t demo_b_count = 0;

static void demo_process_a(void) {
    while (1) {
        demo_a_count++;
        for (volatile int i = 0; i < 500000; i++);
    }
}

static void demo_process_b(void) {
    while (1) {
        demo_b_count++;
        for (volatile int i = 0; i < 700000; i++);
    }
}

uint32_t process_demo_a_count(void) { return demo_a_count; }
uint32_t process_demo_b_count(void) { return demo_b_count; }
void    *process_demo_a_fn(void) { return (void *)demo_process_a; }
void    *process_demo_b_fn(void) { return (void *)demo_process_b; }

static pcb_t   proc_table[MAX_PROCESSES];
static uint8_t proc_stacks[MAX_PROCESSES][STACK_SIZE];
static uint32_t next_pid = 1;
static int      proc_count = 0;

void process_init(void) {
    for (int i = 0; i < MAX_PROCESSES; i++) {
        proc_table[i].state = PROC_UNUSED;
    }
    proc_count = 0;
}

int create_process(void (*entry)(void), const char *name) {
    if (proc_count >= MAX_PROCESSES) return -1;

    int slot = -1;
    for (int i = 0; i < MAX_PROCESSES; i++) {
        if (proc_table[i].state == PROC_UNUSED) { slot = i; break; }
    }
    if (slot == -1) return -1;

    uint8_t *stack_top = proc_stacks[slot] + STACK_SIZE;
    uint32_t *sp = (uint32_t *)stack_top;

    *(--sp) = (uint32_t)entry;
    *(--sp) = 0x202;
    *(--sp) = 0;
    *(--sp) = 0;
    *(--sp) = 0;
    *(--sp) = 0;
    *(--sp) = 0;
    *(--sp) = 0;
    *(--sp) = 0;
    *(--sp) = 0;

    pcb_t *p = &proc_table[slot];
    p->pid        = next_pid++;
    p->state      = PROC_READY;
    p->esp        = (uint32_t)sp;
    p->stack_base = proc_stacks[slot];

    int i = 0;
    while (name[i] && i < 15) { p->name[i] = name[i]; i++; }
    p->name[i] = '\0';

    proc_count++;
    return slot;
}

pcb_t *process_table_get(int index) {
    if (index < 0 || index >= MAX_PROCESSES) return 0;
    return &proc_table[index];
}

int process_table_count(void) {
    return MAX_PROCESSES;
}
