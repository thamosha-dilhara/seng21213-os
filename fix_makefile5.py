content = open('Makefile').read()

old = "                   kernel/race_demo.c"
new = "                   kernel/race_demo.c \\\n                   kernel/prodcons.c"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('Makefile', 'w').write(content)
print("Makefile updated with prodcons.c")
