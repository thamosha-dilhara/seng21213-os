#include "fs.h"
#include "ramdisk.h"

/* ---------------------------------------------------------------------------
 * On-disk layout:
 *   Block 0        - superblock
 *   Block 1        - directory (array of dirent_t)
 *   Block 2        - inode table (array of inode_t)
 *   Block 3        - block bitmap  (1 bit per data block)
 *   Block 4        - inode bitmap (1 bit per inode)
 *   Block 5..255   - data blocks
 * ------------------------------------------------------------------------- */
#define SB_BLOCK        0
#define DIR_BLOCK       1
#define INODE_BLOCK     2
#define BLOCK_BMP_BLK   3
#define INODE_BMP_BLK   4
#define DATA_START      5

#define FS_MAGIC        0x53454E47u  /* 'SENG' */

typedef struct {
    uint32_t magic;
    uint32_t total_blocks;
    uint32_t total_inodes;
} superblock_t;

typedef struct {
    char     name[FS_MAX_NAME];
    uint32_t inode;
    uint8_t  used;
} dirent_t;

typedef struct {
    uint32_t size;
    uint8_t  used;
    uint32_t direct[FS_MAX_DIRECT];
} inode_t;

/* ---- tiny local string helpers (freestanding, no libc) ---- */
static int fs_strcmp(const char *a, const char *b) {
    while (*a && (*a == *b)) { a++; b++; }
    return (uint8_t)*a - (uint8_t)*b;
}
static void fs_strcpy(char *dst, const char *src, int max) {
    int i = 0;
    while (src[i] && i < max - 1) { dst[i] = src[i]; i++; }
    dst[i] = '\0';
}

static dirent_t *get_dir(void)   { return (dirent_t *)ramdisk_block_ptr(DIR_BLOCK); }
static inode_t  *get_inodes(void){ return (inode_t  *)ramdisk_block_ptr(INODE_BLOCK); }
static uint8_t  *get_block_bmp(void) { return ramdisk_block_ptr(BLOCK_BMP_BLK); }
static uint8_t  *get_inode_bmp(void) { return ramdisk_block_ptr(INODE_BMP_BLK); }

static int bmp_test(uint8_t *bmp, uint32_t idx) { return bmp[idx / 8] & (1 << (idx % 8)); }
static void bmp_set(uint8_t *bmp, uint32_t idx)   { bmp[idx / 8] |= (1 << (idx % 8)); }
static void bmp_clear(uint8_t *bmp, uint32_t idx) { bmp[idx / 8] &= ~(1 << (idx % 8)); }

static int alloc_data_block(void) {
    uint8_t *bmp = get_block_bmp();
    for (uint32_t b = DATA_START; b < TOTAL_BLOCKS; b++) {
        if (!bmp_test(bmp, b)) { bmp_set(bmp, b); return (int)b; }
    }
    return -1;
}

static void free_data_block(uint32_t b) {
    bmp_clear(get_block_bmp(), b);
}

static int alloc_inode(void) {
    uint8_t *bmp = get_inode_bmp();
    for (uint32_t i = 0; i < FS_MAX_FILES; i++) {
        if (!bmp_test(bmp, i)) { bmp_set(bmp, i); return (int)i; }
    }
    return -1;
}

static dirent_t *find_dirent(const char *name) {
    dirent_t *dir = get_dir();
    for (int i = 0; i < FS_MAX_FILES; i++) {
        if (dir[i].used && fs_strcmp(dir[i].name, name) == 0) return &dir[i];
    }
    return 0;
}

static dirent_t *find_free_dirent(void) {
    dirent_t *dir = get_dir();
    for (int i = 0; i < FS_MAX_FILES; i++) {
        if (!dir[i].used) return &dir[i];
    }
    return 0;
}

void fs_init(void) {
    ramdisk_init();

    superblock_t *sb = (superblock_t *)ramdisk_block_ptr(SB_BLOCK);
    sb->magic = FS_MAGIC;
    sb->total_blocks = TOTAL_BLOCKS;
    sb->total_inodes = FS_MAX_FILES;

    /* Mark metadata blocks (0-4) permanently used in the block bitmap. */
    uint8_t *bmp = get_block_bmp();
    for (uint32_t b = 0; b < DATA_START; b++) bmp_set(bmp, b);
}

int fs_create(const char *name) {
    if (find_dirent(name)) return -1;   /* already exists */

    dirent_t *slot = find_free_dirent();
    if (!slot) return -1;               /* directory full */

    int inode_idx = alloc_inode();
    if (inode_idx < 0) return -1;       /* no free inodes */

    inode_t *inodes = get_inodes();
    inode_t *ino = &inodes[inode_idx];
    ino->size = 0;
    ino->used = 1;
    for (int i = 0; i < FS_MAX_DIRECT; i++) ino->direct[i] = 0;

    fs_strcpy(slot->name, name, FS_MAX_NAME);
    slot->inode = (uint32_t)inode_idx;
    slot->used  = 1;
    return 0;
}

int fs_write(const char *name, const char *data, uint32_t len) {
    dirent_t *d = find_dirent(name);
    if (!d) return -1;

    inode_t *ino = &get_inodes()[d->inode];
    uint32_t written = 0;

    while (written < len) {
        uint32_t offset_in_file = ino->size;
        uint32_t block_idx = offset_in_file / BLOCK_SIZE;
        uint32_t offset_in_block = offset_in_file % BLOCK_SIZE;

        if (block_idx >= FS_MAX_DIRECT) break;  /* file too large */

        if (ino->direct[block_idx] == 0) {
            int nb = alloc_data_block();
            if (nb < 0) break;               /* disk full */
            ino->direct[block_idx] = (uint32_t)nb;
        }

        uint8_t *blk = ramdisk_block_ptr(ino->direct[block_idx]);
        blk[offset_in_block] = (uint8_t)data[written];

        ino->size++;
        written++;
    }
    return (int)written;
}

int fs_read(const char *name, char *buf, uint32_t buf_size) {
    dirent_t *d = find_dirent(name);
    if (!d) return -1;

    inode_t *ino = &get_inodes()[d->inode];
    uint32_t to_read = ino->size;
    if (to_read > buf_size - 1) to_read = buf_size - 1;

    for (uint32_t i = 0; i < to_read; i++) {
        uint32_t block_idx = i / BLOCK_SIZE;
        uint32_t offset_in_block = i % BLOCK_SIZE;
        uint8_t *blk = ramdisk_block_ptr(ino->direct[block_idx]);
        buf[i] = (char)blk[offset_in_block];
    }
    buf[to_read] = '\0';
    return (int)to_read;
}

int fs_unlink(const char *name) {
    dirent_t *d = find_dirent(name);
    if (!d) return -1;

    inode_t *ino = &get_inodes()[d->inode];
    for (int i = 0; i < FS_MAX_DIRECT; i++) {
        if (ino->direct[i] != 0) {
            free_data_block(ino->direct[i]);
            ino->direct[i] = 0;
        }
    }
    ino->size = 0;
    ino->used = 0;
    bmp_clear(get_inode_bmp(), d->inode);

    d->used = 0;
    return 0;
}

int fs_list(char out_names[][FS_MAX_NAME], uint32_t *out_sizes, int max_entries) {
    dirent_t *dir = get_dir();
    inode_t  *inodes = get_inodes();
    int count = 0;
    for (int i = 0; i < FS_MAX_FILES && count < max_entries; i++) {
        if (dir[i].used) {
            fs_strcpy(out_names[count], dir[i].name, FS_MAX_NAME);
            out_sizes[count] = inodes[dir[i].inode].size;
            count++;
        }
    }
    return count;
}
