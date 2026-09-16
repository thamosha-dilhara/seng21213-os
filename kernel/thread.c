#include "thread.h"
#include "process.h"

/* In this simple kernel, a "thread" reuses the same PCB/stack mechanism
 * as a process (Stage 1). Real threads would share one address space
 * and only get their own stack -- here every task already gets its own
 * 4 KB stack, so thread_create is a thin wrapper for clarity in Stage 2. */
int thread_create(void (*fn)(void), const char *name) {
    return create_process(fn, name);
}
