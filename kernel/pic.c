/* PIC (8259) remap ? moves hardware IRQs 0-15 to interrupt vectors 32-47
 * so they don't clash with CPU exception vectors 0-31. */
#include "pic.h"
#include "io.h"

#define PIC1_COMMAND 0x20
#define PIC1_DATA    0x21
#define PIC2_COMMAND 0xA0
#define PIC2_DATA    0xA1

void pic_remap(void) {
    uint8_t mask1 = inb(PIC1_DATA);
    uint8_t mask2 = inb(PIC2_DATA);

    outb(PIC1_COMMAND, 0x11);
    io_wait();
    outb(PIC2_COMMAND, 0x11);
    io_wait();

    outb(PIC1_DATA, 0x20);   /* master IRQs start at vector 32 */
    io_wait();
    outb(PIC2_DATA, 0x28);   /* slave IRQs start at vector 40 */
    io_wait();

    outb(PIC1_DATA, 0x04);
    io_wait();
    outb(PIC2_DATA, 0x02);
    io_wait();

    outb(PIC1_DATA, 0x01);
    io_wait();
    outb(PIC2_DATA, 0x01);
    io_wait();

    (void)mask1;
    (void)mask2;

    /* Mask all IRQs except IRQ0 (timer). The keyboard driver polls
     * directly instead of using interrupts, so IRQ1 stays masked —
     * we have no handler installed for it. */
    outb(PIC1_DATA, 0xFE);   /* 11111110 = only IRQ0 unmasked */
    outb(PIC2_DATA, 0xFF);   /* all slave IRQs masked */
}
