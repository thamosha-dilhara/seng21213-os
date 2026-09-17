content = open('kernel/kernel.c').read()

old1 = '''#include "../include/pmm.h"'''
new1 = '''#include "../include/pmm.h"
#include "../include/fs.h"'''

old2 = '''    pmm_init();'''
new2 = '''    pmm_init();
    fs_init();'''

old3 = '''static void cmd_meminfo(void);'''
new3 = '''static void cmd_meminfo(void);
static void cmd_ls(void);
static void cmd_touch(const char *name);
static void cmd_cat(const char *name);
static void cmd_write(const char *args);
static void cmd_rm(const char *name);'''

old4 = '''static void cmd_mem(void) {'''
new4 = '''static void cmd_ls(void) {
    char names[FS_MAX_FILES][FS_MAX_NAME];
    uint32_t sizes[FS_MAX_FILES];
    int count = fs_list(names, sizes, FS_MAX_FILES);

    vga_puts_color("\\n  RAM Disk Files\\n", VGA_LIGHT_CYAN, VGA_BLACK);
    vga_puts("  ---------------------------------------\\n");
    if (count == 0) {
        vga_puts("  (no files)\\n\\n");
        return;
    }
    for (int i = 0; i < count; i++) {
        vga_puts("  ");
        vga_puts(names[i]);
        vga_puts("   ");
        print_uint(sizes[i]);
        vga_puts(" bytes\\n");
    }
    vga_puts("\\n");
}

static void cmd_touch(const char *name) {
    if (k_strlen(name) == 0) {
        vga_puts_color("  Usage: touch <name>\\n", VGA_YELLOW, VGA_BLACK);
        return;
    }
    if (fs_create(name) == 0) {
        vga_puts("  Created: "); vga_puts(name); vga_puts("\\n");
    } else {
        vga_puts_color("  Error: could not create file (exists or full)\\n", VGA_LIGHT_RED, VGA_BLACK);
    }
}

static void cmd_cat(const char *name) {
    if (k_strlen(name) == 0) {
        vga_puts_color("  Usage: cat <name>\\n", VGA_YELLOW, VGA_BLACK);
        return;
    }
    static char buf[4097];
    int n = fs_read(name, buf, sizeof(buf));
    if (n < 0) {
        vga_puts_color("  Error: file not found\\n", VGA_LIGHT_RED, VGA_BLACK);
        return;
    }
    vga_puts("\\n");
    vga_puts(buf);
    vga_puts("\\n\\n");
}

static void cmd_write(const char *args) {
    static char name[FS_MAX_NAME];
    int i = 0;
    while (args[i] && args[i] != ' ' && i < FS_MAX_NAME - 1) {
        name[i] = args[i];
        i++;
    }
    name[i] = '\\0';

    if (i == 0 || args[i] != ' ') {
        vga_puts_color("  Usage: write <name> <text>\\n", VGA_YELLOW, VGA_BLACK);
        return;
    }
    const char *text = k_ltrim(args + i);

    int written = fs_write(name, text, (uint32_t)k_strlen(text));
    if (written < 0) {
        vga_puts_color("  Error: file not found (use touch first)\\n", VGA_LIGHT_RED, VGA_BLACK);
    } else {
        vga_puts("  Wrote "); print_uint((uint32_t)written); vga_puts(" bytes to "); vga_puts(name); vga_puts("\\n");
    }
}

static void cmd_rm(const char *name) {
    if (k_strlen(name) == 0) {
        vga_puts_color("  Usage: rm <name>\\n", VGA_YELLOW, VGA_BLACK);
        return;
    }
    if (fs_unlink(name) == 0) {
        vga_puts("  Removed: "); vga_puts(name); vga_puts("\\n");
    } else {
        vga_puts_color("  Error: file not found\\n", VGA_LIGHT_RED, VGA_BLACK);
    }
}

static void cmd_mem(void) {'''

old5 = '''if (k_strcmp(cmd, "meminfo")     == 0) { cmd_meminfo(); continue; }'''
new5 = '''if (k_strcmp(cmd, "meminfo")     == 0) { cmd_meminfo(); continue; }
        if (k_strcmp(cmd, "ls")          == 0) { cmd_ls();      continue; }

        if (k_strncmp(cmd, "touch ", 6) == 0) { cmd_touch(k_ltrim(cmd + 6)); continue; }
        if (k_strncmp(cmd, "cat ", 4)   == 0) { cmd_cat(k_ltrim(cmd + 4));   continue; }
        if (k_strncmp(cmd, "write ", 6) == 0) { cmd_write(k_ltrim(cmd + 6)); continue; }
        if (k_strncmp(cmd, "rm ", 3)    == 0) { cmd_rm(k_ltrim(cmd + 3));    continue; }'''

old6 = '''if (k_strcmp(cmd, "kill")    == 0 ||
            k_strcmp(cmd, "threads") == 0 ||
            k_strcmp(cmd, "free")    == 0 ||
            k_strcmp(cmd, "ls")      == 0 ||
            k_strcmp(cmd, "cat")     == 0) {'''
new6 = '''if (k_strcmp(cmd, "kill")    == 0 ||
            k_strcmp(cmd, "threads") == 0 ||
            k_strcmp(cmd, "free")    == 0) {'''

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
print("Stage 4 filesystem commands added: ls, touch, cat, write, rm")
