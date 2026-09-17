content = open('Makefile').read()

old = "                   kernel/prodcons.c"
new = "                   kernel/prodcons.c \\\n                   kernel/pmm.c"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('Makefile', 'w').write(content)
print("Makefile updated with pmm.c")
