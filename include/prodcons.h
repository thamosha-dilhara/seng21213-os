#ifndef PRODCONS_H
#define PRODCONS_H

#include "types.h"

void      prodcons_reset(void);
void     *prodcons_producer_fn(void);
void     *prodcons_consumer_fn(void);
int       prodcons_finished(void);
int       prodcons_corruption_detected(void);
uint32_t  prodcons_items_produced(void);
uint32_t  prodcons_items_consumed(void);
int       prodcons_debug_empty(void);
int       prodcons_debug_full(void);
int       prodcons_debug_mutex_locked(void);
int       prodcons_debug_producer_done(void);
int       prodcons_debug_consumer_done(void);

#endif
