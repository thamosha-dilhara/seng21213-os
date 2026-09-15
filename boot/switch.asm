[bits 32]

; void switch_context(uint32_t *old_esp_store, uint32_t new_esp)
;   old_esp_store ? pointer to where we save the CURRENT stack pointer
;   new_esp       ? the stack pointer to switch TO

global switch_context
switch_context:
    mov eax, [esp+4]      ; eax = old_esp_store pointer
    mov edx, [esp+8]      ; edx = new_esp value

    pushf                 ; save flags of the outgoing process
    pusha                 ; save all general registers

    mov [eax], esp        ; save outgoing process's stack pointer
    mov esp, edx          ; switch to incoming process's stack

    popa                  ; restore incoming process's registers
    popf                  ; restore incoming process's flags

    ret                   ; resume incoming process where it left off
