<div align="center">

# Sutra-1 / সুত্র-1 / सूत्र-1

*Simple 10-bit CPU from scratch*

<img src="https://raw.githubusercontent.com/rnayabed/sutra-1/refs/heads/master/screenshots/main.png" alt="Sutra-1 Main Screenshot">

### [Demonstration Video](https://youtu.be/MTGICKC4G5U)

</div>

## Introduction

I wanted to apply the concepts I had learnt in my Digital Systems classes and put together a basic turing machine. Projects such as [Nand2Tetris](https://www.nand2tetris.org/) and [Ben Eater's 8-bit Breadboard computer](https://www.youtube.com/@BenEater) also motivated me to make my own. 

Due to no prior knowledge in VHDL and being a beginner in the world of Digital Systems, I used [Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution) to build the system. 

I insisted on building every discrete component from scratch (instead of using built-in components) and with NAND gates only, to keep myself true to the Nand2Tetris course.

## Components

This project is consists of two parts
- Hardware: The main digital logic design, made in Logisim Evolution, saved as `sutra_1.circ` 
- Software
    - রচয়িতা / Rochoyita `rochoyita.py`: Simple assembler that converts mnemonics into binary instructions and compiles them into a Logisim-Evolution compatible memory image.
    - শিল্পী / Shilpi `shipli.py`: Simple 1-bit image generator for the 64x32 demo screen included.

## Specifications

- Single core, in-order, non pipelined
- RISC design: All instructions are 10-bits and executed within one cycle
- 10-bit data bus
- 20-bit address bus
- 1 General Purpose Shift Register and Accumulator(A)
- 3 General Purpose Registers (B, C, D)
- Flag Based ALU with hardware NAND/ADD/SUBTRACT
- IO
    - 64x32 1-bit display
    - 4 interrupt lines
    - 10-bit output bus
- Stack support
- Hardware and Software Interrupts with Masking support





Note: outdated README. needs to be updated.

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
