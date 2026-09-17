content = open('include/ramdisk.h').read()

old = "#define TOTAL_BLOCKS  256"
new = "#define TOTAL_BLOCKS  32   /* 32 x 4KB = 128 KB -- kept small so the\n                              * kernel's BSS doesn't grow past the VGA\n                              * buffer at physical 0xB8000. */"

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('include/ramdisk.h', 'w').write(content)
print("ramdisk.h shrunk to 128KB to avoid VGA memory overlap.")
