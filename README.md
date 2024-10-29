# Sutra-1

A computer system built from scratch.

## Goals

- NAND gates only (SN74HC00N)
- Simple, RISC-like design
- Most instructions should take one clock cycle.

## Specifications

- Single core, in-order, non pipelined
- 10 bit data bus
- 20 bit address bus
- Little endian
- Hardware substraction and addition

## Components

Upper limit: 2400 NAND gates (600 ICs)

Note: the values marked with ~ are approximate.

- 1 Accumulator                 (PIPO Universal Shift register)     ~210    (55)
- 3 General register            (normal register)                   ~40x3   (30)
- 1 MAR (20 bit)                (normal register w/ 20 bits)        ~80     (20)
- 1 Stack pointer (10 bit)      (normal register w/ 10 bits)        ~40     (10)
- 1 PC Load Register (20 bit)   (normal register w/ 20 bits)        ~80     (20)
- 1 Program counter (20 bit)    (sync counter)                      ~500    (125)
- ALU                                                               ~410    (103)
- ALU Result register
- ALU Result Flags register (zero, negative, carry)
- Instruction Register (part of Control unit?)
- ALU Flags register            (normal register w/ 3 bits)         ~12     (3)
- Interrupt Status Register     (normal register w/ 4 bits)         ~16     (4)
- Interrupt Mask Register       (normal register w/ 4 bits)         ~16     (4)
                                                                            (384)

- Control Unit                                                      ~300    (75)

Remaining: ~564 (141)

## Calling Convention

### Initialise

- Push PC
- Push A
- Push B
- Push C
- Push D
- Push local variable n (max tbd)
- Push local variable n-1
- Push local variable n-2
...
- Push local variable 1

### Unwind (return)

- Pop n variables
- Pop D -> Store in Register D
- Pop C -> Store in Register C
- Pop B -> Store in Register B
- Pop A -> Store in Register A
- Pop PC -> Store in PC 

Normal execution continues 

### Store local variable to register

- Caculate offset "SP - (variable number)"
- Store result to MAR
- Store memory output to Register (read)

### Store register value to local variable 

- Caculate offset "SP - (variable number)"
- Store result to MAR
- Write register value to memory (write)


### Notes

- Instead of having a specific register to store Return value. we will use a specific address in memory


NEED TO REMOVE FLAG #37 (CLEAR ISR)