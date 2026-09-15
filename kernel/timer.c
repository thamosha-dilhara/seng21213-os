#include "timer.h"
#include "pit.h"
#include "io.h"
#include "scheduler.h"

static volatile uint32_t timer_ticks = 0;

void timer_init(uint32_t frequency) {
    pit_init(frequency);
}

void irq0_handler(void) {
    timer_ticks++;
    outb(0x20, 0x20);   /* End-of-Interrupt to master PIC -- must happen
                          * BEFORE the context switch, or the PIC never
                          * gets told the interrupt was handled and the
                          * timer will not fire again. */
    scheduler_tick();
}

uint32_t timer_get_ticks(void) {
    return timer_ticks;
}
