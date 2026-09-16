#ifndef RACE_DEMO_H
#define RACE_DEMO_H

#include "types.h"

void      race_demo_reset(int with_mutex);
void     *race_demo_a_fn(void);
void     *race_demo_b_fn(void);
int       race_demo_finished(void);
uint32_t  race_demo_value(void);
uint32_t  race_demo_expected(void);

#endif
