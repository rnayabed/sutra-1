# Memory

Everything is stored in one 20-bit x 10-bit memory (1 Mega Binary Words).

| Type | From Address | To Address | No. of words |
|---|---|---|---|
| Program | 00000 | FF7FF | 1048576 |
| Interrupt Service Routine | FF800 | FFE0B | 1548 |
| Stack | FFE0C | FFFFF | 500 |
| **TOTAL** | **00000** | **FFFFF** | **1048576** |