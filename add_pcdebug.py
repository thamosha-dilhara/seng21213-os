content = open('kernel/kernel.c').read()

old1 = '''static void cmd_prodcons(void);'''
new1 = '''static void cmd_prodcons(void);
static void cmd_pcdebug(void);'''

old2 = '''static void cmd_mem(void) {'''
new2 = '''static void cmd_pcdebug(void) {
    vga_puts_color("\\n  Producer-Consumer debug state\\n", VGA_LIGHT_CYAN, VGA_BLACK);
    vga_puts("  sem_empty count: "); print_uint((uint32_t)prodcons_debug_empty());
    vga_puts("\\n  sem_full  count: "); print_uint((uint32_t)prodcons_debug_full());
    vga_puts("\\n  mutex locked:    "); print_uint((uint32_t)prodcons_debug_mutex_locked());
    vga_puts("\\n  producer done:   "); print_uint((uint32_t)prodcons_debug_producer_done());
    vga_puts("\\n  consumer done:   "); print_uint((uint32_t)prodcons_debug_consumer_done());
    vga_puts("\\n  produced so far: "); print_uint(prodcons_items_produced());
    vga_puts("\\n  consumed so far: "); print_uint(prodcons_items_consumed());
    vga_puts("\\n\\n");
}

static void cmd_mem(void) {'''

old3 = '''if (k_strcmp(cmd, "prodcons")    == 0) { cmd_prodcons(); continue; }'''
new3 = '''if (k_strcmp(cmd, "prodcons")    == 0) { cmd_prodcons(); continue; }
        if (k_strcmp(cmd, "pcdebug")     == 0) { cmd_pcdebug();  continue; }'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"
assert old3 in content, "PATTERN 3 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
content = content.replace(old3, new3)
open('kernel/kernel.c', 'w').write(content)
print("pcdebug command added.")
