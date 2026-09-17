#ifndef RAMDISK_H
#define RAMDISK_H

#include "types.h"

#define BLOCK_SIZE    4096
#define TOTAL_BLOCKS  32   /* 32 x 4KB = 128 KB -- kept small so the
                              * kernel's BSS doesn't grow past the VGA
                              * buffer at physical 0xB8000. */

void      ramdisk_init(void);
uint8_t  *ramdisk_block_ptr(uint32_t block_num);

#endif
