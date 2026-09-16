content = open('kernel/mutex.c').read()

old = '''        __asm__ __volatile__("sti");
        /* Spin -- the timer interrupt (still enabled here) will fire
         * and let the scheduler run other tasks while we wait. */
    }'''

new = '''        __asm__ __volatile__("sti");
        __asm__ __volatile__("hlt");
        /* hlt pauses the CPU until the next interrupt (the timer),
         * guaranteeing the scheduler gets a chance to run other tasks
         * instead of racing to re-lock cli before the tick can land. */
    }'''

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('kernel/mutex.c', 'w').write(content)
print("mutex.c fixed with hlt in spin loop.")
