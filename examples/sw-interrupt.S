LOADI B 1
LOADI C 4
:loop
LOADI A 1
ALUFSETO ADD
ALUEVAL B
ALUSTORER B
COPY B A
ALUFSETO AND
ALUEVAL C
JZ :loop

// Commenting below line will simply halt execution
// ISR will not be executed and B will be set to 888
LOADISR 1000 
LOADI B 888   
HALT

:ISR
ILOCKSET 1
LOADI B 999
LOADISR 0000
ILOCKSET 0
HALT