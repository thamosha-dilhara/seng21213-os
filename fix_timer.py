content = open('kernel/timer.c').read()

old1 = '#include "timer.h"\n#include "pit.h"\n#include "io.h"'
new1 = '#include "timer.h"\n#include "pit.h"\n#include "io.h"\n#include "scheduler.h"'

old2 = '''void irq0_handler(void) {
    timer_ticks++;
    outb(0x20, 0x20);   /* End-of-Interrupt to master PIC */
}'''
new2 = '''void irq0_handler(void) {
    timer_ticks++;
    outb(0x20, 0x20);   /* End-of-Interrupt to master PIC -- must happen
                          * BEFORE the context switch, or the PIC never
                          * gets told the interrupt was handled and the
                          * timer will not fire again. */
    scheduler_tick();
}'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
open('kernel/timer.c', 'w').write(content)
print("timer.c updated with scheduler hook.")
