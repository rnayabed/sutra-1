# rochoyita - simple assembler for sutra-1

import math

input_file_name = 'input.sutra-1'
output_file_name = 'image'

class Instruction:
    def __init__(self, op_code, operands=()):
        self.op_code = op_code
        self.operands = operands

class Operand:
    def __init__(self, type, length):
        self.type = type
        self.length = length

class OperandType(enum.Enum):
    DESTINATION = 1
    SOURCE = 2
    DATA = 3

instructions = {
    'COPY'      : Instruction(
        '0001',
        (
            Operand(OperandType.SOURCE,         3),
            Operand(OperandType.DESTINATION,    3)
        )
    ),
    'LOADIL'    : Instruction(
        '010',
        (
            Operand(OperandType.DESTINATION,    2),
            Operand(OperandType.DATA,           5)
        )
    ),
    'LOADIU'    : Instruction(
        '001',
        (
            Operand(OperandType.DESTINATION,    2),
            Operand(OperandType.DATA,           5)
        )
    ),
    'ALUFSET'   : Instruction(
        '011',
        (
            Operand(OperandType.DATA,           7)
        )
    ),
    'ALUEVAL'   : Instruction(
        '1000000',
        (
            Operand(OperandType.SOURCE,         3)
        )
    ),
    'ALUSTOREF' : Instruction(
        '1000010',
        (
            Operand(OperandType.DESTINATION,    3)
        )
    ),
    'ALUSTORER' : Instruction(
        '1000100',
        (
            Operand(OperandType.DESTINATION,    3)
        )
    ),
    'STORE'     : Instruction(
        '1000110',
        (
            Operand(OperandType.SOURCE,         3)
        )
    ),
    'LOAD'      : Instruction(
        '1001000',
        (
            Operand(OperandType.DESTINATION,    3)
        )
    ),
    'ACCU'      : Instruction(
        '10010100',
        (
            Operand(OperandType.DATA,           2)
        )
    ),
    'JUMP'      : Instruction(
        '10011000',
        (
            Operand(OperandType.DATA,           2)
        )
    ),
    'OUT'       : Instruction(
        '1001110',
        (
            Operand(OperandType.SOURCE,         3)
        )
    ),
    'CLEARISR'  : Instruction('1010000000'),
    'ALUFSET'   : Instruction(
        '10100100',
        (
            Operand(OperandType.SOURCE,         2)
        )
    ),
    'NOOP'      : Instruction('0000000000'),
    'HALT'      : Instruction('1111111111')
}

destination_registers = ('A', 'B', 'C', 'D', 'SP', 'IMR', 'MARL', 'MARH')
source_registers = ('A', 'B', 'C', 'D', 'SP', 'IMR', 'ISR')


def error(line_number, line, error):
    print(f'ERROR line #{line_number}: "{line}"')
    print(error)
    exit(1)

line_number = 0

output = []

source_file = open(input_file_name, 'r')
for line in source_file:
    line_number +=1

    if line.startswith('#'):
        continue # Ignore comments

    tokens = line.strip().upper().split()
    
    if tokens[0] not in instructions:
        error(line_number, line, f'"{tokens[0]}" is not a valid instruction')
        exit(1)

    instruction = instructions[tokens[0]]

    if (len(tokens) - 1) != len(instruction.operands):
        error(line_number, line, f'operands mismatch. expected {len(instruction.operands)}, given {len(tokens) - 1}')

    output_instruction = instruction.op_code

    for i in range(1, len(tokens)):

        operand_info = instruction.operands[i]

        token = tokens[i]
        
        if operand_info.length != len(token):
            error(line_number, line, f'operand "{token}" length mismatch. expected {operand_info.length}, given {len(token)}')
        
        if operand_info.type == OperandType.DESTINATION:
            output_instruction += format(destination_registers.index(token), 'b')
        elif operand_info.type == OperandType.SOURCE:
            output_instruction += format(source_registers.index(token), 'b')
        elif operand_info.type == OperandType.DATA:
            if any(c not in '01' for c in token):
                error(line_number, line, f'"{token}" is not a valid binary number')
            output_instruction += token

    if len(output_instruction) != 10:
        error(line_number, line, f'resultant assembled instruction {output_line} exceeds max length')
        
    output.append(format(int(output_instruction, 2), 'X'))
source_file.close()

# generate output
output_file = open(output_file_name, 'w')
output_lines = ['v3.0 hex words addressed']

index = 0


output_file.writelines(output_lines)
output_file.close()