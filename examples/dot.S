/*
Simple program to move a pixel across the 64x32 screen

For more information about the screen, refer to https://github.com/rnayabed/sutra-1/blob/master/docs/screen.md

Screen commands:
select row and column   01<row bank:2><column index:6>
row data                10<data:8>
load buffer             1100000000
*/

// Row data is stored in D
// Row bank and column index in C

// Start from center
// column 31, row 15
LOADI C b0001011111
LOADI D b0010000000


// render
:render
LOADISR  0000
ILOCKSET 0

ALUFSETO ADD

// select row bank and column
LOADI A b0100000000
ALUEVAL C
ALUSTORER A
OUT A

// output row data
LOADI A b1000000000
ALUEVAL D
ALUSTORER A
OUT A

// load buffer
LOADI A b1100000000
OUT A





// keep looping
:loop
NOOP        // Check if this is even needed?
J :loop




// handle input
:ISR
ILOCKSET 1

// first, zero the current value
LOADI A b1000000000
OUT A




// ISR maps: UP DOWN LEFT RIGHT
/* masking trick, OC & NAND */

COPY ISR B
ALUFSETO AND




:up
LOADI A b0000001000
ALUEVAL B
JZ :down


/*
if row_data = 0010000000, +1 to row_bank, row_data = 1
else simply left shift row_data
*/

// check if already at end
LOADI A b0010000000
ALUEVAL D
JZ :up-normal

COPY C A

LOADI B b0001000000
ALUFSETO ADD
ALUEVAL B
ALUSTORER A

LOADI B b0011111111
ALUFSETO AND
ALUEVAL B
ALUSTORER C

LOADI D 1
J :render

:up-normal
// left shift row data
COPY D A
AOPT SLEFT
COPY A D

J :render




:down
LOADI A b0000000100
ALUEVAL B
JZ :left


/*
if row_data = 0000000001, -1 from row_bank, row_data = 10000000
else simply left shift row_data
*/

// check if already at end
LOADI A b0000000001
ALUEVAL D
JZ :down-normal

COPY C A

LOADI B b0001000000
ALUFSETO SUB
ALUEVAL B
ALUSTORER A

LOADI B b0011111111
ALUFSETO AND
ALUEVAL B
ALUSTORER C

LOADI D b0010000000
J :render

:down-normal
// right shift row data
COPY D A
AOPT SRIGHT
COPY A D

J :render





:left
LOADI A b0000000010
ALUEVAL B
JZ :right


ALUFSET 0000011
ALUEVAL C
ALUSTORER B

LOADI A b0000111111
ALUFSETO AND
ALUEVAL B
ALUSTORER B

LOADI A b0011000000
ALUEVAL C
ALUSTORER A

ALUFSETO ADD
ALUEVAL B
ALUSTORER C


J :render



:right
LOADI A b0000000001
ALUEVAL B
JZ :render

LOADI A 1
ALUFSETO ADD
ALUEVAL C
ALUSTORER B

LOADI A b0000111111
ALUFSETO AND
ALUEVAL B
ALUSTORER B

LOADI A b0011000000
ALUEVAL C
ALUSTORER A

ALUFSETO ADD
ALUEVAL B
ALUSTORER C

J :render