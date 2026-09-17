#include "pmm.h"

/* E820 map, written by the bootloader (boot/boot.asm) at physical 0x8000:
 *   offset 0 : uint16_t entry_count
 *   offset 4 : entries, 20 bytes each -- base(8) length(8) type(4) */
#define E820_ADDR       0x8000
#define E820_TYPE_USABLE 1

/* Bitmap covers up to 32 MB of physical memory = 8192 frames = 1024 bytes */
#define MAX_FRAMES      8192
#define FRAME_SIZE      4096

static uint8_t  bitmap[MAX_FRAMES / 8];
static uint32_t total_frames = 0;
static uint32_t used_frames  = 0;

typedef struct {
    uint32_t base_low;
    uint32_t base_high;
    uint32_t length_low;
    uint32_t length_high;
    uint32_t type;
} __attribute__((packed)) e820_entry_t;

static void bitmap_set(uint32_t frame) {
    bitmap[frame / 8] |= (1 << (frame % 8));
}

static void bitmap_clear(uint32_t frame) {
    bitmap[frame / 8] &= ~(1 << (frame % 8));
}

static int bitmap_test(uint32_t frame) {
    return bitmap[frame / 8] & (1 << (frame % 8));
}

void pmm_init(void) {
    /* Start with everything marked used; we'll free the usable E820
     * regions below. This is the safe default for any memory the E820
     * map doesn't explicitly describe (reserved/BIOS/unknown). */
    for (uint32_t i = 0; i < MAX_FRAMES / 8; i++) {
        bitmap[i] = 0xFF;
    }
    total_frames = 0;
    used_frames  = 0;

    uint16_t entry_count = *(uint16_t *)E820_ADDR;
    e820_entry_t *entries = (e820_entry_t *)(E820_ADDR + 4);

    for (uint16_t i = 0; i < entry_count; i++) {
        e820_entry_t *e = &entries[i];
        if (e->base_high != 0 || e->length_high != 0) continue; /* ignore >4GB */
        if (e->type != E820_TYPE_USABLE) continue;

        uint32_t start_frame = e->base_low / FRAME_SIZE;
        uint32_t frame_count = e->length_low / FRAME_SIZE;

        for (uint32_t f = start_frame; f < start_frame + frame_count; f++) {
            if (f >= MAX_FRAMES) break;
            bitmap_clear(f);
            if (f + 1 > total_frames) total_frames = f + 1;
        }
    }

    /* Reserve the first 1 MB (BIOS, boot sector, kernel image, our own
     * stacks) regardless of what E820 reports -- it is never safe to
     * hand out to pmm_alloc_frame(). */
    uint32_t reserve_frames = (1024 * 1024) / FRAME_SIZE;
    for (uint32_t f = 0; f < reserve_frames && f < MAX_FRAMES; f++) {
        bitmap_set(f);
    }

    used_frames = 0;
    for (uint32_t f = 0; f < total_frames; f++) {
        if (bitmap_test(f)) used_frames++;
    }
}

uint32_t pmm_alloc_frame(void) {
    for (uint32_t f = 0; f < total_frames; f++) {
        if (!bitmap_test(f)) {
            bitmap_set(f);
            used_frames++;
            return f * FRAME_SIZE;
        }
    }
    return 0;  /* out of memory */
}

void pmm_free_frame(uint32_t frame_addr) {
    uint32_t f = frame_addr / FRAME_SIZE;
    if (f >= total_frames) return;
    if (bitmap_test(f)) {
        bitmap_clear(f);
        used_frames--;
    }
}

uint32_t pmm_total_frames(void) { return total_frames; }
uint32_t pmm_used_frames(void)  { return used_frames; }
uint32_t pmm_free_frames(void)  { return total_frames - used_frames; }
