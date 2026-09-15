content = open('kernel/process.c').read()

old = "    proc_count++;\n    return p->pid;"
new = "    proc_count++;\n    return slot;"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('kernel/process.c', 'w').write(content)
print("process.c now returns slot index.")
