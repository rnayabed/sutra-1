# Interrupts

Sutra-1 implements a basic 4-line interrupt system with masking and software invoke/clear support.

## Interrupt Service Routine

Interrupt Service Routine starts at address `0xFF800`. It can have a maximum of 1548 native instructions.

To declare an ISR, we will need simply need  

[!WARNING]  
> If an ISR is not provided and an interrupt is triggered, execution will be halted.

## Examples

- [hw-interrupt.S](https://github.com/rnayabed/sutra-1/blob/master/examples/hw-interrupt.S)
- [sw-interrupt.S](https://github.com/rnayabed/sutra-1/blob/master/examples/sw-interrupt.S)
- [dot.S](https://github.com/rnayabed/sutra-1/blob/master/examples/dot.S)
