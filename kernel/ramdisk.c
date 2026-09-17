#include "ramdisk.h"

static uint8_t disk[BLOCK_SIZE * TOTAL_BLOCKS];

void ramdisk_init(void) {
    for (uint32_t i = 0; i < sizeof(disk); i++) disk[i] = 0;
}

uint8_t *ramdisk_block_ptr(uint32_t block_num) {
    if (block_num >= TOTAL_BLOCKS) return 0;
    return &disk[(uint32_t)block_num * BLOCK_SIZE];
}
