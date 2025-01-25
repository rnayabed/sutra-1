//#include "include-pre.S"
// 10 + 15 = 25 stored in C

LOADI A 50
ALUFSETO SUB
ALUEVAL C
ALUSTORER D     // 50 if #include is removed/commented, 25 otherwise
HALT