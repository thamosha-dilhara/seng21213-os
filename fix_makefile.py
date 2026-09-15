content = open('Makefile').read()

old1 = "KERNEL_ASM_SRC := kernel/kernel_entry.asm kernel/idt_asm.asm\nKERNEL_ASM_OBJ := build/kernel_entry.o build/idt_asm.o"
new1 = "KERNEL_ASM_SRC := kernel/kernel_entry.asm kernel/idt_asm.asm boot/switch.asm\nKERNEL_ASM_OBJ := build/kernel_entry.o build/idt_asm.o build/switch.o"

old2 = "                   kernel/timer.c"
new2 = "                   kernel/timer.c    \\\n                   kernel/process.c"

old3 = "build/%.o: kernel/%.asm"
new3 = "build/%.o: kernel/%.asm\n\t@mkdir -p build\n\t@echo \"  [AS]  $<\"\n\t$(AS) $(ASFLAGS) $< -o $@\n\nbuild/%.o: boot/%.asm"

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"
assert old3 in content, "PATTERN 3 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
content = content.replace(old3, new3)

open('Makefile', 'w').write(content)
print("Makefile updated for process.c and switch.asm.")
