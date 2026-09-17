content = open('kernel/kernel.c').read()

old1 = '''#include "../include/prodcons.h"'''
new1 = '''#include "../include/prodcons.h"
#include "../include/pmm.h"'''

old2 = '''    process_init();
    scheduler_init();'''
new2 = '''    pmm_init();

    process_init();
    scheduler_init();'''

old3 = '''static void cmd_pcdebug(void);'''
new3 = '''static void cmd_pcdebug(void);
static void cmd_meminfo(void);'''

old4 = '''static void cmd_mem(void) {'''
new4 = '''static void cmd_meminfo(void) {
    uint32_t total = pmm_total_frames();
    uint32_t used  = pmm_used_frames();
    uint32_t free_ = pmm_free_frames();

    vga_puts_color("\\n  Physical Memory Manager\\n", VGA_LIGHT_CYAN, VGA_BLACK);
    vga_puts("  ---------------------------------------\\n");
    vga_puts("  Total frames: "); print_uint(total);
    vga_puts(" ("); print_uint(total * 4); vga_puts(" KB)\\n");
    vga_puts("  Used frames:  "); print_uint(used);
    vga_puts(" ("); print_uint(used * 4); vga_puts(" KB)\\n");
    vga_puts("  Free frames:  "); print_uint(free_);
    vga_puts(" ("); print_uint(free_ * 4); vga_puts(" KB)\\n\\n");
}

static void cmd_mem(void) {'''

old5 = '''if (k_strcmp(cmd, "pcdebug")     == 0) { cmd_pcdebug();  continue; }'''
new5 = '''if (k_strcmp(cmd, "pcdebug")     == 0) { cmd_pcdebug();  continue; }
        if (k_strcmp(cmd, "meminfo")     == 0) { cmd_meminfo(); continue; }'''

old6 = '''if (k_strcmp(cmd, "ps")      == 0 ||
            k_strcmp(cmd, "kill")    == 0 ||
            k_strcmp(cmd, "threads") == 0 ||
            k_strcmp(cmd, "free")    == 0 ||
            k_strcmp(cmd, "ls")      == 0 ||
            k_strcmp(cmd, "cat")     == 0) {'''
new6 = '''if (k_strcmp(cmd, "kill")    == 0 ||
            k_strcmp(cmd, "threads") == 0 ||
            k_strcmp(cmd, "free")    == 0 ||
            k_strcmp(cmd, "ls")      == 0 ||
            k_strcmp(cmd, "cat")     == 0) {'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"
assert old3 in content, "PATTERN 3 NOT FOUND"
assert old4 in content, "PATTERN 4 NOT FOUND"
assert old5 in content, "PATTERN 5 NOT FOUND"
assert old6 in content, "PATTERN 6 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
content = content.replace(old3, new3)
content = content.replace(old4, new4)
content = content.replace(old5, new5)
content = content.replace(old6, new6)
open('kernel/kernel.c', 'w').write(content)
print("meminfo command added, ps stub removed from milestone list.")
