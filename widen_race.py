content = open('kernel/race_demo.c').read()

old = '''        } else {
            uint32_t tmp = unsafe_global;
            tmp = tmp + 1;
            unsafe_global = tmp;
        }'''

new = '''        } else {
            uint32_t tmp = unsafe_global;
            for (volatile int d = 0; d < 50; d++);  /* widen the race window */
            tmp = tmp + 1;
            unsafe_global = tmp;
        }'''

count = content.count(old)
assert count == 2, "EXPECTED 2 MATCHES, FOUND " + str(count)
content = content.replace(old, new)
open('kernel/race_demo.c', 'w').write(content)
print("race_demo.c race window widened.")
