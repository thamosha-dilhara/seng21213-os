content = open('Makefile').read()

old = "                   kernel/semaphore.c"
new = "                   kernel/semaphore.c \\\n                   kernel/race_demo.c"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('Makefile', 'w').write(content)
print("Makefile updated with race_demo.c")
