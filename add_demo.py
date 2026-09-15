content = open('kernel/process.c').read()

old = '#include "process.h"\n#include "vga.h"'
new = '''#include "process.h"
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
void    *process_demo_b_fn(void) { return (void *)demo_process_b; }'''

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('kernel/process.c', 'w').write(content)
print("Demo processes added to process.c")
