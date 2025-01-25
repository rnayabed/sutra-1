J :main

:sum
ALUFSETO ADD
COPY C A
ALUEVAL D
ALUSTORER D     // D = C + D
RETURN

:main
// value will be restored after return
// cannot be used as argument
LOADI A 12
LOADI B 522

// value will be restored after return
// can be used as argument
LOADI C 420

// value will NOT be restored after return
// can be used as argument
// result will be stored here
LOADI D 69

CALL :sum

// A = 12
// B = 522
// C = 420
// D should be equal to 420 + 69 = 489
HALT



