lines = open('kernel/process.c').read().split('\n')

entry_idx = None
eflags_idx = None
for i, line in enumerate(lines):
    if 'uint32_t)entry' in line:
        entry_idx = i
    if '0x202' in line:
        eflags_idx = i

assert entry_idx is not None, "ENTRY LINE NOT FOUND"
assert eflags_idx is not None, "EFLAGS LINE NOT FOUND"

eflags_line = lines.pop(eflags_idx)
insert_at = entry_idx + 1 if eflags_idx > entry_idx else entry_idx
lines.insert(insert_at, eflags_line)

open('kernel/process.c', 'w').write('\n'.join(lines))
print("process.c stack order fixed successfully.")
print("New order (entry area):")
for l in lines[entry_idx-1:entry_idx+11]:
    print(" ", l)
