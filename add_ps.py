content = open('kernel/kernel.c').read()

old1 = '''static void cmd_mem(void);
static void cmd_ticks(void);'''

new1 = '''static void cmd_mem(void);
static void cmd_ticks(void);
static void cmd_ps(void);'''

old2 = '''static void cmd_mem(void) {'''

new2 = '''static void print_uint(uint32_t v) {
    char buf[12];
    int i = 0;
    if (v == 0) { vga_putchar('0'); return; }
    while (v > 0) { buf[i++] = '0' + (v % 10); v /= 10; }
    while (i > 0) { vga_putchar(buf[--i]); }
}

static void cmd_ps(void) {
    vga_puts_color("\\n  PID  NAME       STATE\\n", VGA_LIGHT_CYAN, VGA_BLACK);
    vga_puts("  ---  ---------  ----------\\n");
    for (int i = 0; i < process_table_count(); i++) {
        pcb_t *p = process_table_get(i);
        if (p->state == PROC_UNUSED) continue;
        vga_puts("  ");
        print_uint(p->pid);
        vga_puts("    ");
        vga_puts(p->name);
        vga_puts("     ");
        switch (p->state) {
            case PROC_READY:      vga_puts("READY");      break;
            case PROC_RUNNING:    vga_puts("RUNNING");    break;
            case PROC_TERMINATED: vga_puts("TERMINATED"); break;
            default: break;
        }
        vga_puts("\\n");
    }
    vga_puts_color("\\n  demo_a progress: ", VGA_LIGHT_GREEN, VGA_BLACK);
    print_uint(process_demo_a_count());
    vga_puts_color("\\n  demo_b progress: ", VGA_LIGHT_GREEN, VGA_BLACK);
    print_uint(process_demo_b_count());
    vga_puts("\\n\\n");
}

static void cmd_mem(void) {'''

old3 = '''if (k_strcmp(cmd, "ticks") == 0) { cmd_ticks(); continue; }'''
new3 = '''if (k_strcmp(cmd, "ticks") == 0) { cmd_ticks(); continue; }
        if (k_strcmp(cmd, "ps")    == 0) { cmd_ps();    continue; }'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"
assert old3 in content, "PATTERN 3 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
content = content.replace(old3, new3)
open('kernel/kernel.c', 'w').write(content)
print("ps command added successfully.")
