content = open('include/process.h').read()

old = "void      process_init(void);"
new = """void      process_init(void);
void     *process_demo_a_fn(void);
void     *process_demo_b_fn(void);
uint32_t  process_demo_a_count(void);
uint32_t  process_demo_b_count(void);"""

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('include/process.h', 'w').write(content)
print("process.h updated with demo function declarations.")
