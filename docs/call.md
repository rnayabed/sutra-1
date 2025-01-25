# Calling convention

Sutra-1 does not have a native instruction for call/return, but a simple one is implemented in rochoyita.

Arguments may be stored in Register C and D and the return value is stored in Register D.

Values of register A, B, C are preserved during `CALL` and is restored after `RETURN`.

## CALL

- Push A, B, C values to stack
- Push return address (sum of current instruction address and length of generated output upto `JUMP`) to stack 
- Store arguments in A, B and C
- Jump to address or label
- Restore register A, B, C values by popping them from stack (executed after `RETURN`)

## RETURN

- Jump to the return address by popping it from stack

## Examples 

- [function.S](https://github.com/rnayabed/sutra-1/blob/master/examples/function.S)