content = open('Makefile').read()

old = "                   kernel/process.c  \\\n                   kernel/scheduler.c"
new = "                   kernel/process.c  \\\n                   kernel/scheduler.c \\\n                   kernel/thread.c    \\\n                   kernel/mutex.c     \\\n                   kernel/semaphore.c"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('Makefile', 'w').write(content)
print("Makefile updated with thread.c, mutex.c, semaphore.c")
