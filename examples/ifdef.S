#define VAL 30

// Uncomment below line to see 200 being loaded
//#undef VAL

#ifdef VAL
    LOADI A 100
#else
    LOADI A 200
#endif
HALT