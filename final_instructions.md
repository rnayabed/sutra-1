# ISA verification status

| Instruction | Verified |
|-------------|----------|
| COPY        |          |
| LOADIL      |    x     |
| LOADIU      |    x     |
| ALUFSET     |          |
| ALUEVAL     |          |
| ALUSTOREF   |          |
| ALUSTORER   |          |
| STORE       |          |
| LOAD        |          |
| ACCU        |          |
| JUMP        |          |
| OUT         |          |
| LOADISR     |          |
| ALUFSETR    |          |
| NOOP        |          |
| HALT        |          |
| ILOCKSET    |          |




## LOADIL

(9-7)           (5-6)           (0-4)
LOADIL[3]       <DESTINATION 2> <DATA 5>
                <A|B|C|D>
010


### Program

LOADIL A 11111      0100011111      11F
LOADIL B 11111      0100111111      13F
LOADIL C 11111      0101011111      15F
LOADIL D 11111      0101111111      17F
HALT                1111111111      3FF

Check if registers A, B, C, D all are equal to

00000 11111
Decimal: 31

## LOADIU

(9-7)           (5-6)           (0-4)
LOADIU[3]       <DESTINATION 2> <DATA 5>
                <A|B|C|D>
001

### Program

LOADIU A 11111      0010011111      9F
LOADIU B 11111      0010111111      BF
LOADIU C 11111      0011011111      DF
LOADIU D 11111      0011111111      FF
HALT                1111111111      3FF

Check if registers A, B, C, D all are equal to

11111 00000
Decimal: 992


## COPY [TBD]

(6-9)           (3-5)       (0-3)
COPY[4]         <SOURCE 3>  <DESTINATION 3>  
000.1

### Program

LOADIU A 11010
LOADIL A 00111

COPY A B
COPY A C
COPY A D
COPY A MARLH
COPY A MARH
COPY A SP
COPY A IMR

## OUT

OUT[7]          <SOURCE 3>
100111.0


