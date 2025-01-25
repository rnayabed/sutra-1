#define NUM_1 50
#define NUM_2 30

LOADI A NUM_1

// Uncommenting the line below will throw an error
//#undef NUM_2    

LOADI B NUM_2
ALUFSETO SUB
ALUEVAL B
ALUSTORER C
HALT