# Instruction Set Architecture

Sutra-1 features 17 main instructions. It also provides 13 pseudo instructions via the Rochoyita assembler program, which expand into multiple main instructions to reduce source code size and improve user experience.

## Native Instructions


| Instruction | OP Code | Syntax | Description |
|---|---|---|---|
| COPY | 0001  | `COPY [Source] [Destination]`<br><br>Source: A, B, C, D, SP, IMR, ISR<br>Destination: A, B, C, D, SP, IMR, MARL, MARH<br><br>Example:<br>`COPY A B` = `00010001`  | Copy data from source to destination register |
| LOADIL | 010  | `COPY [Destination] [Data]`<br><br> Destination: A, B, C, D  | Assign the lower bits (0-4) of destination register |
| LOADIU | 001  | `COPY [Destination] [Data]`<br><br> Destination: A, B, C, D  | Assign the upper bits (5-9) of destination register |
| ALUFSET | 011  | `ALUFSET [Flags]`<br><br>ALU flags (Descending bit order)<br>• OC: Complement Output<br>• N: NAND instead of ADD<br>• Cin: Input carry for ADD<br>• BC: Complement B<br>• BZ: Zero B<br>• AC: Complement A<br>• AZ: Zero A<br><br>Note:<br>• The BZ flag is evaluated before BC.<br>• The AZ flag is evaluated before AC.<br>• The Cin flag is ignored in NAND mode  <br><br>Example:<br>`ALUFSET 1000010` will configure ALU to perform `A - [Source register]`  | Configure the Arithmetic Logic unit|
| ALUFSETR | 10100100 | `ALUFSETR [Source]`<br><br>Source: A, B, C, D | Sets ALU flags from source register |
| ALUEVAL | 1000000 | `ALUEVAL [Source]`<br><br>Source: A, B, C, D, SP, IMR, ISR | Perform ALU operation and save result in the ALU Results Register. The first operand (A) is register A, and the second operand, B is the source register |
| ALUSTOREF | 1000010 | `ALUSTOREF [Destination]`<br><br>Destination: A, B, C, D, SP, IMR, MARL, MARH | Store the ALU flags to destination register |
| ALUSTORER | 1000100 | `ALUSTORER [Destination]`<br><br>Destination: A, B, C, D, SP, IMR, MARL, MARH | Store ALU result to destination register |
| AOP | 10010100 | `AOP [Mode]`<br><br>Modes:<br>• 00: Do nothing<br>• 01: Shift right<br>• 10: Shift left<br>• 11: Load | Select operation mode of register A |
| STORE | 1000110 | `STORE [Source]`<br><br>Source: A, B, C, D, SP, IMR, ISR | Stores value of source register to address in memory, pointed by Memory Address Register (MAR) |
| LOAD | 1001000 | `LOAD [Destination]`<br><br>Destination: A, B, C, D, SP, IMR, MARL, MARH | Loads value from memory pointed by Memory Address Register (MAR) to destination register |
| JUMP | 10011000 | `JUMP [Mode]`<br><br>Modes:<br>• `00`: Unconditional<br>• `01`: If Zero<br>• `10`: If Negative<br>• `11`: If Carry | Jump Program Counter (PC) to address pointed by Memory Address Register (MAR) |
| OUT | 1001110 | `OUT [Source]`<br><br>Source: A, B, C, D, SP, IMR, ISR | Outputs data stored in source register to data bus and enables output bus |
| LOADISR | 101000 | `LOADISR [I3][I2][I1][I0]` | Set Interrupt Status Register (ISR) flags |
| ILOCKSET | 101010000 | `ILOCKSET [Flag]`<br><br>Flag:<br>• `0`: Set lock<br>• `1`: Remove lock | Sets Interrupt lock and prevents interrupts from triggering jump |
| NOOP | 0000000000  | `NOOP` | No operation |
| HALT | 1111111111  | `HALT` | Disables Program Counter (PC) and halts execution |

## Pseudo Instructions


| Instruction | Syntax | Description |
|---|---|---|
| LOADI | `LOADI [Source] [Data]`<br><br>Source: A, B, C, D<br><br>Data format types:<br>• `b[data]` for binary<br>• `h[data]` for hex<br>• `o[data]` for octal<br>• `[data]` for decimal | Loads a full 10-bit value to source register (0 to 1023) |
| LOADI_SIGNED | `LOADI_SIGNED [Source] [Data]`<br><br>Source: A, B, C, D<br><br>Data format types:<br>• `b[data]` for binary<br>• `h[data]` for hex<br>• `o[data]` for octal<br>• `[data]` for decimal | Signed version of LOADI (-512 to 511) |
| ALUFSETO | `ALUFSETO [Option]`<br><br>Options:<br>• ADD<br>• SUB: A - B<br>• SUB_REV: B – A<br>• NAND<br>• NOT (B’)<br>• NOT_A (A’)<br>• AND<br><br>Note: B here refers to the register selected during ALUEVAL | Sets a fixed set of flags for corresponding option
| LOADMARI | `LOADMARI [:label or address`<br><br>Loads memory address to Memory Address Register (MAR). Labels can be used too. | Uses register A for loading purpose |
| STACKPUSH | `STACKPUSH [Source]`<br><br>Source: A, B, C, D, SP, IMR, ISR | Push value to stack |
| STACKPOP | `STACKPOP [Destination]`<br><br>Destination: A, B, C, D, SP, IMR, MARL, MARH | Pop value from stack |
| CALL | `CALL [:label or address]` | Preserve values of register A, B, C and D to stack and jump to a routine |
| RETURN | `RETURN` | Return from a routine to original location and restore values of register A, B, C and D |
| AOPT | `AOPT [Option]`<br><br>Options:<br>• `SLEFT`: Shift left<br>• `SRIGHT`: Shift Right | Perform shift operation on register A |
| J | `J [:label or address]` | Jump unconditionally |
| JZ | `JZ [:label or address]` | Jump if zero bit of ALU result flags is set |
| JN | `JN [:label or address]` | Jump if negative bit of ALU result flags is set |
| JC | `JC [:label or address]` | Jump if carry it of ALU result flags is set |


