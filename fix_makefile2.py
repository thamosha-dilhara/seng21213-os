content = open('Makefile').read()

old = "                   kernel/timer.c    \\\n                   kernel/process.c"
new = "                   kernel/timer.c    \\\n                   kernel/process.c  \\\n                   kernel/scheduler.c"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('Makefile', 'w').write(content)
print("Makefile updated with scheduler.c")
