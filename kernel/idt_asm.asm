[bits 32]

global idt_flush
idt_flush:
    mov eax, [esp+4]
    lidt [eax]
    ret

global irq0
extern irq0_handler

irq0:
    pusha
    call irq0_handler
    popa
    iret
