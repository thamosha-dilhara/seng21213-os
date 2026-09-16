content = open('kernel/kernel.c').read()

old = '''    while (!prodcons_finished()) {
        __asm__ __volatile__("hlt");
    }'''

new = '''    uint32_t wait_loops = 0;
    while (!prodcons_finished()) {
        __asm__ __volatile__("hlt");
        wait_loops++;
        if (wait_loops > 2000) {
            vga_puts_color("\\n  [TIMEOUT] Not finished after waiting. Debug state:\\n",
                           VGA_LIGHT_RED, VGA_BLACK);
            vga_puts("  sem_empty count: "); print_uint((uint32_t)prodcons_debug_empty());
            vga_puts("\\n  sem_full  count: "); print_uint((uint32_t)prodcons_debug_full());
            vga_puts("\\n  mutex locked:    "); print_uint((uint32_t)prodcons_debug_mutex_locked());
            vga_puts("\\n  producer done:   "); print_uint((uint32_t)prodcons_debug_producer_done());
            vga_puts("\\n  consumer done:   "); print_uint((uint32_t)prodcons_debug_consumer_done());
            vga_puts("\\n  produced so far: "); print_uint(prodcons_items_produced());
            vga_puts("\\n  consumed so far: "); print_uint(prodcons_items_consumed());
            vga_puts("\\n\\n");
            return;
        }
    }'''

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('kernel/kernel.c', 'w').write(content)
print("cmd_prodcons timeout debug added.")
