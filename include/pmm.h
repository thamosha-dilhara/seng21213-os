#ifndef PMM_H
#define PMM_H

#include "types.h"

void      pmm_init(void);
uint32_t  pmm_alloc_frame(void);
void      pmm_free_frame(uint32_t frame_addr);
uint32_t  pmm_total_frames(void);
uint32_t  pmm_used_frames(void);
uint32_t  pmm_free_frames(void);

#endif
