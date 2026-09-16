content = open('include/prodcons.h').read()

old = "uint32_t  prodcons_items_consumed(void);"
new = """uint32_t  prodcons_items_consumed(void);
int       prodcons_debug_empty(void);
int       prodcons_debug_full(void);
int       prodcons_debug_mutex_locked(void);
int       prodcons_debug_producer_done(void);
int       prodcons_debug_consumer_done(void);"""

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('include/prodcons.h', 'w').write(content)
print("prodcons.h debug declarations added.")
