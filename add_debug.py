content = open('kernel/prodcons.c').read()

old = '''void     *prodcons_producer_fn(void) { return (void *)producer; }
void     *prodcons_consumer_fn(void) { return (void *)consumer; }
int       prodcons_finished(void) { return producer_done && consumer_done; }
int       prodcons_corruption_detected(void) { return corruption; }
uint32_t  prodcons_items_produced(void) { return produced_count; }
uint32_t  prodcons_items_consumed(void) { return consumed_count; }'''

new = '''void     *prodcons_producer_fn(void) { return (void *)producer; }
void     *prodcons_consumer_fn(void) { return (void *)consumer; }
int       prodcons_finished(void) { return producer_done && consumer_done; }
int       prodcons_corruption_detected(void) { return corruption; }
uint32_t  prodcons_items_produced(void) { return produced_count; }
uint32_t  prodcons_items_consumed(void) { return consumed_count; }
int       prodcons_debug_empty(void) { return sem_empty.count; }
int       prodcons_debug_full(void) { return sem_full.count; }
int       prodcons_debug_mutex_locked(void) { return buf_mutex.locked; }
int       prodcons_debug_producer_done(void) { return producer_done; }
int       prodcons_debug_consumer_done(void) { return consumer_done; }'''

assert old in content, "PATTERN NOT FOUND"
content = content.replace(old, new)
open('kernel/prodcons.c', 'w').write(content)
print("prodcons.c debug functions added.")
