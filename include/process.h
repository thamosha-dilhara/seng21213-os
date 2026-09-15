#ifndef PROCESS_H
#define PROCESS_H

#include "types.h"

#define MAX_PROCESSES   8
#define STACK_SIZE      4096   /* 4 KB per process */

typedef enum {
    PROC_UNUSED = 0,
    PROC_READY,
    PROC_RUNNING,
    PROC_TERMINATED
} proc_state_t;

typedef struct {
    uint32_t     pid;
    proc_state_t state;
    uint32_t     esp;          /* saved stack pointer (context switch) */
    uint8_t     *stack_base;   /* base of this process's 4 KB stack */
    char         name[16];
} pcb_t;

void      process_init(void);
void     *process_demo_a_fn(void);
void     *process_demo_b_fn(void);
uint32_t  process_demo_a_count(void);
uint32_t  process_demo_b_count(void);
int       create_process(void (*entry)(void), const char *name);
pcb_t    *process_table_get(int index);
int       process_table_count(void);

#endif
