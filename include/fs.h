#ifndef FS_H
#define FS_H

#include "types.h"

#define FS_MAX_NAME    28
#define FS_MAX_FILES   32
#define FS_MAX_DIRECT  8

void fs_init(void);
int  fs_create(const char *name);
int  fs_write(const char *name, const char *data, uint32_t len);
int  fs_read(const char *name, char *buf, uint32_t buf_size);
int  fs_unlink(const char *name);
int  fs_list(char out_names[][FS_MAX_NAME], uint32_t *out_sizes, int max_entries);

#endif
