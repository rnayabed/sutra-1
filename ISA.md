WHY DOES IT WORK???
stuff i did:
1. sync counter enable is triggered in decode, not fetch mode
    this caused first instruction to be missed. investigate why
2. flags always on even when low clock (check if this is even needed)














# Instruction Set Architecture

ISA for the Sutra-1

## Goals

- Very minimal setup - attempt to perform most tasks with code / pseudo instructions
- Attempt 1 machine cycle wherever possible
- KISS : Keep it simple, stupid

## Accumulator modes

S1  S2
0   0   Shift left
0   1   Shift right
1   0   Load
1   1   Clear

## Components

Load immediate destinations:
A, B, C, D
= 4 (2 bits)

Copy sources:
A, B, C, D, SP, IMR, ISR
= 7 (3 bits)

Copy destinations:
A, B, C, D, SP, IMR, MARL, MARH
= 8 (3 bits) 







A OUT: #7      6
B OUT: #14      13
C OUT: #17      16
D OUT: #20      19
ISR OUT: #23    22
IMR OUT: #24    23
SP OUT: #27     26





Copy destinations:
A, B, C, D, SP, IMR, MARL, MARH
= 8 (3 bits) 

A LOAD LOW:
Flags: #8, #10

A LOAD HIGH:
Flags: #9, #10

B LOAD LOW: #12
B LOAD HIGH: #13

C LOAD LOW: #15
C LOAD HIGH: #16

D LOAD LOW: #18
D LOAD HIGH: #19

IMR LOAD: #22

SP LOAD LOW: #25
SP LOAD HIGH: #26

MARL LOAD LOW: #32
MARL LOAD HIGH #33

MARH LOAD LOW: #34
MARH LOAD HIGH: #35





ALU source/destinations:
(COPY too?)
A, B, C, D, MARL, MARH, SP, IMR
= 8 (3 bits)





All registers:
A, B, C, D, SP, ISR, IMR, MARL, MARH


In:
[A(Acc), B, C, D, SP, ISR, IMR, MARL, MARH]

Out:
[A(Acc), B, C, D, SP, ISR, IMR]
#7, #14, #17, #20, #27, #23, #24

- ALU
    - ALU Flags set
    - ALU Evaluate
    - Store ALU Result
    - Store ALU Result flags
- Information transfer
    - Copy
        - From, To 
    - Load immediate
        - Half Upper
        - Half upper
    - Store
        - Destination address (must be preloaded to MAR)
    - Load from Address
        - Source address (must be preloaded to MAR)
- Accumulator operations
    - Shift left
    - Shift right
    - Load regular
    - Clear
- Jump 
    - To label (address) (must be preloaded to MAR)
    - Conditionals
        - If [not] carry/zero/negative
- Direct Write to Bus

## Instructions

987
(6-9)           (3-5)       (0-3)
COPY[4]         <SOURCE 3>  <DESTINATION 3>  
000.1

(9-7)           (5-6)           (0-4)
LOADIL[3]       <DESTINATION 2> <DATA 5>
010

LOADIU[3]       <DESTINATION 2> <DATA 5>
001


(7-9)           (0-6)
ALUFSET[3]      <FLAGS 7>
011

ALU flags:
6 - output compliment
5 - NAND
4 - Carry in
3 - B compliment
2 - B zero
1 - A compliment
0 - A zero

non ground flags for source
#5, #3, #4, #36, #30
2 3 4 29 35

non ground flags for destination
#2, #1, #36, #31
0 1 30 35


***
ALUEVAL[7]      <SOURCE B 3>
100000.0
#5, #3, #4

***
ALUSTOREF[7]    <DESTINATION 3>
100001.0
#2

***
ALUSTORER[7]    <DESTINATION 3>
100010.0
#1

***
STORE[7]        <SOURCE 3>
100011.0
#36, #30

***
LOAD[7]         <DESTINATION 3>
100100.0
#36, #31

ACCU[8]         <MODE 2>
100101.00

JUMP[8]         <TYPE 2>
100110.00
#36, #28

JUMP MODES:
b1 b0   
0   0   unconditional
0   1   if zero
1   0   if negative
1   1   if carry 

OUT[7]          <SOURCE 3>
100111.0

LOADISR [10]       
101000.0000
#37, #21

ALUFSETR[8]         <SOURCE 2>
101001.00
#6
    
NOOP[10]
0000000000

HALT[10]
1111111111

ILOCKSET[9]     <BIT>
10101.0000      X

## Machine Cycle

(MACHINE CYCLE)

(HIGH)
#1 high     PC OUT
            MEM OUT
            IR IN

#1 low      PC OUT
            MEM OUT
            IR IN

#2 high     control flags based on IR
            PC enable (incr/load) if not HLT

#2 low      control flags based on IR
            PC enable (incr/load) if not HLT


<!-- timeline:
#1 low      incremented PC is selected (1)
#1 high     nothing changes (0 control flags), PC is to be loaded next falling edge
#2 low      PC is loaded
#2 high     nothing changes, PC set to increase next falling edge, control logic changes to take effect next falling edge
 -->


new timeline if rising edge triggered?
#1 low      PC OUT, MEM OUT, IR IN (change to next next rising edge), PC to be incremented next rising edge
#1 high     changes from prev
#2 low      
#2 high     PC is incremented


#1 low      PC OUT, MEM OUT, IR IN,    PC enable            0   0
#1 high     changes                     PC enable           1   U
#2 low      decode                                          1   U                
#2 high     changes                

#1 = decode
#2 = fetch


CLK     MACHINE CYCLE
low     #2                  PC OUT, MEM IN, IR IN, IR will be incremented next step! (CLK 0, EN 1)      (CLK 0, EN 0)
high    #1                  IR loaded, decode                                        (CLK 1, EN 0)      (CLK 1, EN 0)
low     #1                  decoded, IR will be incremented next step                (CLK 0, EN 0)
high    #2                  IR incremented & PC OUT, MEM IN, IR IN                   (CLK 1, EN 1)
low     #2                  PC OUT, MEM IN, IR IN                                    (CLK 0, EN 1)
high    #1
low     #1


work:
fix JK FF (use D ltches instead of SR)
fix sync counter



<!-- (HIGH)
#1 high     fetch & decode
            PC OUT, MEMORY OUT, IR IN, 
            #29, #31

(LOW)
#2 high     control flags
            PC increment if not HLT

#2 low      control flags -->

## Instructions - Machine cycles

ALUFSET
- ALU_FLAGS IN
- IR (3-9) OUT

#6, #37

ALUEVAL
1. SOURCE OUT, ALU B ENABLE, ALU_RESULT LOAD



ALUSTORE
1. ALU_RESULT OUT, SOURCE UPPER IN, SOURCE LOWER IN

ALUSTOREF
1. ALU_RESULT_FLAGS OUT, SOURCE UPPER IN, SOURCE LOWER IN

COPY
1. SOURCE OUT, DESTINATION IN

LOADI
1. SOURCE UPPER/LOWER IN, IR (4-9) OUT

STORE 
1. MAR -> MEMORY, MEMORY IN, SOURCE OUT

LOAD
1. MAR -> MEMORY, MEMORY OUT, SOURCE OUT

ACCU
1. ACCU MODE (Shift Left/Right, Clear)

JUMP
1. MAR -> PC (If type passes)

OUT
1. SOURCE OUT

NOOP
1. No flags enabled 

HALT
1. PC Disable 

## Control Flags

1. ALU_RESULT OUT
2. ALU_RESULT_FLAGS OUT
3. ALU_RESULT LOAD
4. ALU_RESULT_FLAGS LOAD
5. ALU B IN 
6. ALU_FLAGS LOAD
7. A OUT
8. A LOAD LOWER
9. A LOAD HIGHER
10. A MODE SELECT 1 (S1)
11. A MODE SELECT 2 (S2)
12. B LOAD LOWER
13. B LOAD HIGHER
14. B OUT
15. C LOAD LOWER
16. C LOAD HIGHER
17. C OUT
18. D LOAD LOWER
19. D LOAD HIGHER
20. D OUT
21. ISR LOAD (0-3)
22. IMR LOAD (0-3)
23. ISR OUT
24. IMR OUT 
25. SP LOAD LOWER
26. SP LOAD HIGHER
27. SP OUT
28. PC LOAD
29. PC OUT
30. MEMORY IN
31. MEMORY OUT
32. MAR LOWER (0-9)       - LOAD LOWER (5-9)
33. MAR LOWER (0-9)       - LOAD HIGHER (0-4)
34. MAR HIGHER (10-19)    - LOAD LOWER (5-9)
35. MAR HIGHER (10-19)    - LOAD HIGHER (0-4)
36. MAR OUT (20 bits at once)
37. IR OUT
38. ILOCK IN

## TODO

Does #37 need to go?


## Program Counter 

Clk is just disabled if HALT is encountered