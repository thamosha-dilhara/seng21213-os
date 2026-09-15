#ifndef SCHEDULER_H
#define SCHEDULER_H

void scheduler_init(void);
void scheduler_add(int pid_slot);
void scheduler_tick(void);
void scheduler_start(void);

#endif
