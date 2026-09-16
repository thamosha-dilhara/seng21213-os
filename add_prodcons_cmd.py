content = open('kernel/kernel.c').read()

old1 = '''#include "../include/race_demo.h"'''

new1 = '''#include "../include/race_demo.h"
#include "../include/prodcons.h"'''

old2 = '''static void cmd_race(int with_mutex);'''

new2 = '''static void cmd_race(int with_mutex);
static void cmd_prodcons(void);'''

old3 = '''static void cmd_mem(void) {'''

new3 = '''static void cmd_prodcons(void) {
    vga_puts_color("\\n  Producer-Consumer demo (bounded buffer, size 5)\\n",
                   VGA_LIGHT_CYAN, VGA_BLACK);
    vga_puts("  ---------------------------------------\\n");
    vga_puts("  Producer makes 20 items, Consumer takes them, using\\n");
    vga_puts("  semaphores (empty/full) and a mutex for the buffer.\\n");
    vga_puts_color("  Running... (watch for a moment)\\n", VGA_YELLOW, VGA_BLACK);

    prodcons_reset();
    create_process((void (*)(void))prodcons_producer_fn(), "producer");
    create_process((void (*)(void))prodcons_consumer_fn(), "consumer");

    for (int i = 0; i < MAX_PROCESSES; i++) {
        pcb_t *p = process_table_get(i);
        if (p->state == PROC_READY &&
            (k_strcmp(p->name, "producer") == 0 || k_strcmp(p->name, "consumer") == 0)) {
            scheduler_add(i);
        }
    }

    while (!prodcons_finished()) {
        __asm__ __volatile__("hlt");
    }

    vga_puts_color("\\n  Items produced: ", VGA_LIGHT_GREEN, VGA_BLACK);
    print_uint(prodcons_items_produced());
    vga_puts_color("\\n  Items consumed: ", VGA_LIGHT_GREEN, VGA_BLACK);
    print_uint(prodcons_items_consumed());

    if (!prodcons_corruption_detected() &&
        prodcons_items_produced() == 20 && prodcons_items_consumed() == 20) {
        vga_puts_color("\\n  RESULT: Correct! All items consumed in order, no corruption.\\n\\n",
                       VGA_LIGHT_GREEN, VGA_BLACK);
    } else {
        vga_puts_color("\\n  RESULT: Corruption detected in buffer!\\n\\n",
                       VGA_LIGHT_RED, VGA_BLACK);
    }
}

static void cmd_mem(void) {'''

old4 = '''if (k_strcmp(cmd, "race_mutex") == 0) { cmd_race(1); continue; }'''
new4 = '''if (k_strcmp(cmd, "race_mutex") == 0) { cmd_race(1); continue; }
        if (k_strcmp(cmd, "prodcons")    == 0) { cmd_prodcons(); continue; }'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"
assert old3 in content, "PATTERN 3 NOT FOUND"
assert old4 in content, "PATTERN 4 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
content = content.replace(old3, new3)
content = content.replace(old4, new4)
open('kernel/kernel.c', 'w').write(content)
print("prodcons command added.")
