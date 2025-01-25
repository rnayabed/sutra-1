# Rochoyita / রচয়িতা

Rochoyita is a rudimentary assembler written for Sutra-1.

## Features

- Preprocessor directives
    - `#define <MACRO> <VALUE>`
    - `#undef`
    - `#include "<file path>"`
    - `#ifdef <MACRO>`
    - `#ifndef <MACRO>`
    - `#else`
    - `#endif`
- Comments
    - Single line: `// ...`
    - Multi line: `/* .. */`
- Labels (with both ahead/before declarations)
- Raw mode which disables pre processor. It is automatically enabled when `.s` file is encountered on non Windows Systems or `--raw` is explicitly passed in arguments.
- [Pseudo instructions](https://github.com/rnayabed/sutra-1/blob/master/docs/ISA.md#Pseudo_Instructions)

## High-level flowchart

```mermaid
graph TD;
    A[Input file]--> B{Raw Mode}
    B--> |No| C[Parse directives]
    B--> |Yes| D
    C-->D[Assemble instructions and preserve list of unresolved labels]
    D-->E[Resolve labels and memory addresses]
    E-->F[Check memory boundary constraints]
    F-->G[Generate Logisim Evolution v3.0 hex file]
```