# Stack

The stack implemented is basic and is part of the main memory itself. The stack pointer is set in a dedicated SP register. It starts at address `0xFFFFF` and grows from the end.

Values can be pushed to stack using `STACKPUSH` and `STACKPOP` pseudo-instructions

# Examples

- [stack.S](https://github.com/rnayabed/sutra-1/blob/master/examples/stack.S)