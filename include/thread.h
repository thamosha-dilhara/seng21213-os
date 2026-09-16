#ifndef THREAD_H
#define THREAD_H

#include "types.h"

int thread_create(void (*fn)(void), const char *name);

#endif
