content = open('Makefile').read()

old = "                   kernel/pmm.c"
new = "                   kernel/pmm.c \\\n                   kernel/ramdisk.c \\\n                   kernel/fs.c"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('Makefile', 'w').write(content)
print("Makefile updated with ramdisk.c and fs.c")
