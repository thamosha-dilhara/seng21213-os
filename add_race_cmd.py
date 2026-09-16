content = open('kernel/kernel.c').read()

old1 = '''#include "../include/process.h"
#include "../include/scheduler.h"'''

new1 = '''#include "../include/process.h"
#include "../include/scheduler.h"
#include "../include/race_demo.h"'''

old2 = '''static void cmd_mem(void);
static void cmd_ticks(void);
static void cmd_ps(void);'''

new2 = '''static void cmd_mem(void);
static void cmd_ticks(void);
static void cmd_ps(void);
static void cmd_race(int with_mutex);'''

old3 = '''static void cmd_mem(void) {'''

new3 = '''static void cmd_race(int with_mutex) {
    vga_puts_color(with_mutex ? "\\n  Race demo WITH mutex\\n" : "\\n  Race demo WITHOUT mutex\\n",
                   VGA_LIGHT_CYAN, VGA_BLACK);
    vga_puts("  ---------------------------------------\\n");
    vga_puts("  Two tasks each increment a shared counter 50000 times.\\n");
    vga_puts_color("  Running... (watch for a moment)\\n", VGA_YELLOW, VGA_BLACK);

    race_demo_reset(with_mutex);
    create_process((void (*)(void))race_demo_a_fn(), "racer_a");
    create_process((void (*)(void))race_demo_b_fn(), "racer_b");
    int a_slot = process_table_count();
    (void)a_slot;

    for (int i = 0; i < MAX_PROCESSES; i++) {
        pcb_t *p = process_table_get(i);
        if (p->state == PROC_READY &&
            (k_strcmp(p->name, "racer_a") == 0 || k_strcmp(p->name, "racer_b") == 0)) {
            scheduler_add(i);
        }
    }

    while (!race_demo_finished()) {
        __asm__ __volatile__("hlt");
    }

    uint32_t final_val = race_demo_value();
    uint32_t expected   = race_demo_expected();

    vga_puts_color("\\n  Expected total: ", VGA_LIGHT_GREEN, VGA_BLACK);
    print_uint(expected);
    vga_puts_color("\\n  Actual total:   ", VGA_LIGHT_GREEN, VGA_BLACK);
    print_uint(final_val);

    if (final_val == expected) {
        vga_puts_color("\\n  RESULT: Correct! No data corruption.\\n\\n", VGA_LIGHT_GREEN, VGA_BLACK);
    } else {
        vga_puts_color("\\n  RESULT: Data corruption detected! Lost updates due to race condition.\\n\\n", VGA_LIGHT_RED, VGA_BLACK);
    }
}

static void cmd_mem(void) {'''

old4 = '''if (k_strcmp(cmd, "ps")    == 0) { cmd_ps();    continue; }'''
new4 = '''if (k_strcmp(cmd, "ps")    == 0) { cmd_ps();    continue; }
        if (k_strcmp(cmd, "race")       == 0) { cmd_race(0); continue; }
        if (k_strcmp(cmd, "race_mutex") == 0) { cmd_race(1); continue; }'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"
assert old3 in content, "PATTERN 3 NOT FOUND"
assert old4 in content, "PATTERN 4 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
content = content.replace(old3, new3)
content = content.replace(old4, new4)
open('kernel/kernel.c', 'w').write(content)
print("race and race_mutex commands added.")
