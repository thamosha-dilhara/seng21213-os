content = open('kernel/semaphore.c').read()

old = '''        __asm__ __volatile__("sti");
        /* Spin -- timer interrupt still enabled, scheduler keeps running
         * other tasks while this one waits for the count to rise. */
    }'''

new = '''        __asm__ __volatile__("sti");
        __asm__ __volatile__("hlt");
        /* hlt pauses the CPU until the next interrupt (the timer),
         * guaranteeing the scheduler gets a chance to run other tasks
         * instead of racing to re-lock cli before the tick can land. */
    }'''

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('kernel/semaphore.c', 'w').write(content)
print("semaphore.c fixed with hlt in spin loop.")
