content = open('kernel/process.c').read()

old = '''    *(--sp) = (uint32_t)entry;  /* return address for final `ret` */
    *(--sp) = 0;                /* eax */
    *(--sp) = 0;                /* ecx */
    *(--sp) = 0;                /* edx */
    *(--sp) = 0;                /* ebx */
    *(--sp) = 0;                /* esp (ignored by popa) */
    *(--sp) = 0;                /* ebp */
    *(--sp) = 0;                /* esi */
    *(--sp) = 0;                /* edi */
    *(--sp) = 0x202;            /* eflags ? IF (interrupt flag) set */'''

new = '''    *(--sp) = (uint32_t)entry;  /* return address, popped last by ret */
    *(--sp) = 0x202;            /* eflags -- IF set, popped by popf */
    *(--sp) = 0;                /* eax */
    *(--sp) = 0;                /* ecx */
    *(--sp) = 0;                /* edx */
    *(--sp) = 0;                /* ebx */
    *(--sp) = 0;                /* esp (ignored by popa) */
    *(--sp) = 0;                /* ebp */
    *(--sp) = 0;                /* esi */
    *(--sp) = 0;                /* edi -- popped FIRST by popa */'''

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('kernel/process.c', 'w').write(content)
print("process.c stack order fixed successfully.")
