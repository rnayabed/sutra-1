<div align="center">

# Sutra-1 / সুত্র-1 / सूत्र-1

*10-bit CPU and Assembler*

<img src="https://raw.githubusercontent.com/rnayabed/sutra-1/refs/heads/master/screenshots/main.png" alt="Sutra-1 Main Screenshot">

### [Demonstration Video](https://youtu.be/2qCsluuu69Y)

</div>

## Introduction

I wanted to apply the concepts I had learnt in my Digital Systems classes and put together a basic turing machine. Projects such as [Nand2Tetris](https://www.nand2tetris.org/) and [Ben Eater's 8-bit Breadboard computer](https://www.youtube.com/@BenEater) also motivated me to make my own. 

Due to no prior knowledge of a Hardware Description Language and being a beginner in the world of Digital Systems, I used [Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution) to build the system. 

I insisted on building every discrete component from scratch (instead of using built-in components) and with NAND gates only, to keep myself true to the Nand2Tetris course. Only the display was built from built-in components as it is considered an I/O device and not a part of the CPU.

## Components

This project is consists of two parts
- Hardware: The main digital logic design, made in Logisim Evolution, saved as `sutra_1.circ` 
- Software
    - রচয়িতা / Rochoyita `rochoyita.py`: Assembler. [Rochoyita Documentation](https://github.com/rnayabed/sutra-1/blob/master/docs/rochoyita.md)
    - শিল্পী / Shilpi `shipli.py`: Image generator for the 64x32 1-bit demo display. [Shilpi Documentation](https://github.com/rnayabed/sutra-1/blob/master/docs/display.md#Shilpi)

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

## Documentation

- [Example programs](https://github.com/rnayabed/sutra-1/blob/master/examples/README.md)
- [Instruction Set Architecture](https://github.com/rnayabed/sutra-1/blob/master/docs/ISA.md)
- [Rochoyita Assembler](https://github.com/rnayabed/sutra-1/blob/master/docs/rochoyita.md)
- [Interrupts](https://github.com/rnayabed/sutra-1/blob/master/docs/interrupts.md)
- [Display](https://github.com/rnayabed/sutra-1/blob/master/docs/display.md)
- [Stack](https://github.com/rnayabed/sutra-1/blob/master/docs/stack.md)
- [Memory](https://github.com/rnayabed/sutra-1/blob/master/docs/stack.md)

## Future plans

- Implement this on an FPGA
- Add pipelining
- Add out of order execution
- Make it superscalar

## Special thanks

- [Nand2Tetris](https://www.nand2tetris.org/)
- [EE102](https://study.iitm.ac.in/es/course_pages/EE1102.html)
- [Lorenzo's Logisim-Evolution Fork](https://github.com/lorenzonotaro/logisim-evolution/tree/main) for faster simulation clock speed

## License

All components and designs are licensed under the [GNU General Public License v3.0](https://github.com/rnayabed/sutra-1/blob/master/LICENSE).