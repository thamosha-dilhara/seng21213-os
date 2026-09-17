content = open('boot/boot.asm').read()

old1 = '''    mov  si, msg_ok
    call print_rm

; ---------------------------------------------------------------------------
; Enter Protected Mode
; ---------------------------------------------------------------------------
enter_pm:'''

new1 = '''    mov  si, msg_ok
    call print_rm

    call detect_memory

; ---------------------------------------------------------------------------
; Enter Protected Mode
; ---------------------------------------------------------------------------
enter_pm:'''

old2 = '''; ---------------------------------------------------------------------------
; Data
; ---------------------------------------------------------------------------
boot_drive  db 0'''

new2 = '''; ---------------------------------------------------------------------------
; Subroutine: detect_memory -- BIOS E820 memory map, stored at physical
; address 0x8000 (count as a word at offset 0, entries of 20 bytes each
; starting at offset 4). Read back by the kernel's PMM in Stage 3.
; ---------------------------------------------------------------------------
detect_memory:
    pusha
    mov  ax, 0x0800
    mov  es, ax
    mov  di, 4
    xor  ebx, ebx
    xor  bp, bp
.e820_loop:
    mov  eax, 0xE820
    mov  ecx, 20
    mov  edx, 0x534D4150
    int  0x15
    jc   .e820_done
    cmp  eax, 0x534D4150
    jne  .e820_done
    inc  bp
    add  di, 20
    cmp  bp, 32
    jae  .e820_done
    test ebx, ebx
    jne  .e820_loop
.e820_done:
    mov  [es:0], bp
    popa
    ret

; ---------------------------------------------------------------------------
; Data
; ---------------------------------------------------------------------------
boot_drive  db 0'''

assert old1 in content, "PATTERN 1 NOT FOUND"
assert old2 in content, "PATTERN 2 NOT FOUND"

content = content.replace(old1, new1)
content = content.replace(old2, new2)
open('boot/boot.asm', 'w').write(content)
print("boot.asm updated with E820 memory detection.")
