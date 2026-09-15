content = open('kernel/kernel.c').read()

old1 = '''#include "vga.h"
#include "keyboard.h"
#include "../include/types.h"
#include "../include/pic.h"
#include "../include/idt.h"
#include "../include/timer.h"'''

new1 = '''#include "vga.h"
#include "keyboard.h"
#include "../include/types.h"
#include "../include/pic.h"
#include "../include/idt.h"
#include "../include/timer.h"
#include "../include/process.h"
#include "../include/scheduler.h"'''

old2 = '''    pic_remap();
    idt_init();
    timer_init(100);
    __asm__ __volatile__("sti");
    print_splash();
    shell_run();'''

new2 = '''    pic_remap();
    idt_init();

    process_init();
    scheduler_init();
    create_process((void (*)(void))process_demo_a_fn(), "demo_a");
    create_process((void (*)(void))process_demo_b_fn(), "demo_b");
    scheduler_add(0);
    scheduler_add(1);
    scheduler_start();

    timer_init(100);
    __asm__ __volatile__("sti");
    print_splash();
    shell_run();'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
open('kernel/kernel.c', 'w').write(content)
print("kernel.c updated with process creation and scheduler start.")
