#!/bin/python
# rochoyita - simple assembler for sutra-1

import math, enum, re, argparse, pathlib, itertools

def error_raw(*text):
    print('\033[1;4;7;31m') # red with blue, underline, inverted text
    print('\n'.join(text))
    print('\033[0m')
    exit(1)

# handle args
parser = argparse.ArgumentParser(
    prog='rochoyita',
    description='Simple assembler from the Sutra-1 System',
    epilog='Copyright (C) 2025 Debayan "rnayabed" Sutradhar'
)

parser.add_argument('-o', '--output')
parser.add_argument('input')
args = parser.parse_args()

input_file_name = args.input
output_file_name = args.output if args.output is not None else input_file_name + '.out'

if not pathlib.Path(input_file_name).is_file():
    error_raw(f'input file "{input_file_name}" not found!')


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
            Operand(OperandType.DATA,           7),
        )
    ),
    'ALUEVAL'   : Instruction(
        '1000000',
        (
            Operand(OperandType.SOURCE,         3),
        )
    ),
    'ALUSTOREF' : Instruction(
        '1000010',
        (
            Operand(OperandType.DESTINATION,    3),
        )
    ),
    'ALUSTORER' : Instruction(
        '1000100',
        (
            Operand(OperandType.DESTINATION,    3),
        )
    ),
    'STORE'     : Instruction(
        '1000110',
        (
            Operand(OperandType.SOURCE,         3),
        )
    ),
    'LOAD'      : Instruction(
        '1001000',
        (
            Operand(OperandType.DESTINATION,    3),
        )
    ),
    'ACCU'      : Instruction(
        '10010100',
        (
            Operand(OperandType.DATA,           2),
        )
    ),
    'JUMP'      : Instruction(
        '10011000',
        (
            Operand(OperandType.DATA,           2),
        )
    ),
    'OUT'       : Instruction(
        '1001110',
        (
            Operand(OperandType.SOURCE,         3),
        )
    ),
    'LOADISR'  : Instruction(
        '101000',
        (
            Operand(OperandType.DATA,           4),
        )
    ),
    'ALUFSETR'   : Instruction(
        '10100100',
        (
            Operand(OperandType.SOURCE,         2),
        )
    ),
    'NOOP'      : Instruction('0000000000'),
    'HALT'      : Instruction('1111111111'),
    'ILOCKSET'  : Instruction(
        '101010000',
        (
            Operand(OperandType.DATA,           1),
        )
    )
}
destination_registers = ('A', 'B', 'C', 'D', 'SP', 'IMR', 'MARL', 'MARH')
source_registers = ('A', 'B', 'C', 'D', 'SP', 'IMR', 'ISR')

def error(line_number, line, error):
    error_raw(
        f'ERROR{' in line #{line_number}' if line_number is not None else ''}: "{line}"',
        error
    )

# pre process
line_number = 0
multi_line_comment_block = False

source_file = open(input_file_name, 'r')
define_replace = {}
source_lines = []
for line in source_file:
    line_number +=1
    line = line.strip()

    if line.startswith('/*'):
        multi_line_comment_block = True

    if line.startswith('//') or multi_line_comment_block or not line:
        source_lines.append(line)
        if line.endswith('*/'):
            multi_line_comment_block = False
        continue # Ignore comments and empty lines

    if line.startswith('#'):  
        tokens = line.split() 
        
        if len(tokens[1]) < 2:
            error(f'invalid preprocessor use')

        if tokens[1].upper() == 'DEFINE': 
            if len(tokens) != 4:
                error(line_number, line, f'"{line} is not a valid pre-processor directive')

            for name, value in define_replace.items():
                tokens[3] = re.sub(rf'\b{name}\b', value, tokens[3])

            define_replace[tokens[2]] = tokens[3]
        else:
            error(line_number, line, f'invalid preprocessor directive "{tokens[1]}"')
    else:
        for name, value in define_replace.items():
            line = re.sub(rf'\b{name}\b', value, line)
    source_lines.append(line)

source_file.close()

# assemble
line_number = 0
multi_line_comment_block = False
output = []

# mnemonic -> hex
def assemble(line, tokens, line_number=None):
    instruction = instructions[tokens[0]]

    print('\033[32mASSEMBLE', line.ljust(20), sep='\t', end='\t')

    if (len(tokens) - 1) != len(instruction.operands):
        error(line_number, line, f'operands mismatch. expected {len(instruction.operands)}, given {len(tokens) - 1}')

    output_instruction = instruction.op_code

    for i in range(len(tokens) - 1):

        operand_info = instruction.operands[i]

        token = tokens[i + 1]
        
        if operand_info.type == OperandType.DESTINATION:
            if token not in destination_registers:
                error(line_number, line, f'"{token}" is not a valid destination register')
            output_instruction += format(destination_registers.index(token), 'b').zfill(operand_info.length)

        elif operand_info.type == OperandType.SOURCE:
            if token not in source_registers:
                error(line_number, line, f'"{token}" is not a valid source register')
            output_instruction += format(source_registers.index(token), 'b').zfill(operand_info.length)
            
        elif operand_info.type == OperandType.DATA:
            if operand_info.length != len(token):
                error(line_number, line, f'operand "{token}" length mismatch. expected {operand_info.length}, given {len(token)}')

            if any(c not in '01' for c in token):
                error(line_number, line, f'"{token}" is not a valid binary number')

            output_instruction += token


    if len(output_instruction) != 10:
        error(line_number, line, f'resultant assembled instruction {output_instruction} does not match standard length')

    hex_ = format(int(output_instruction, 2), 'X')
    print(output_instruction, hex_ + '\033[0m', sep='\t')

    return (hex_,)

# Pseudo assemble: mnemonic -> another mnemonic

def pseudo_assemble_loadi(line, tokens, line_number=None, signed=True):
    # LOADI <destination:2> <value>

    if len(tokens) != 3:
        error(line, line_number, f'invalid {'LOADI' if signed else 'LOADI_UNSIGNED'} syntax')
    
    destination = tokens[1]
    value_str = tokens[2]

    # # Add common verification block
    # if destination_str not in destination_registers:
    #     error(line_number, line, f'invalid destination register "{destination_str}"')

    # index = destination_registers.index(destination_str)
    # TODO: add this type in assemble?
    # if index > 2**2:
    #     error(line_number, line, f'destination register "{destination_str}" not allowed. it must be between {', '.join(destination_registers[i] for i in range(2**2))}')
    # destination = format(index, 'b').zfill(2)

    try:
        value_int = int(value_str)
        if signed:
            if value_int < -512 or value_int > 511:
                error(line_number, line, f'invalid integer {value_str} - range must be between -512 and 511 (inclusive)')

            value = format(abs(value_int), 'b').zfill(10)
            if value_int < 0:
                value = ''.join('1' if c == '0' else '0' for c in value)
                value = format(int(value, 2) + 1, 'b')
        else:
            if value_int < 0 or value_int > 1023:
                error(line_number, line, f'invalid integer {value_str} - range must be between 0 and 1023 (inclusive)')

            value = format(abs(value_int), 'b').zfill(10)           

    except Exception as e:
        error(line_number, line, f'{value_str} is not a valid integer')

    value_upper = value[:5]
    value_lower = value[5:]

    output_mnemonics = (
        f'LOADIU {destination} {value_upper}',
        f'LOADIL {destination} {value_lower}'  
    )

    return (itertools.chain(*(assemble(m, m.split()) for m in output_mnemonics)))

def pseudo_assemble_loadi_unsigned(line, tokens, line_number=None):
    return pseudo_assemble_loadi(line, tokens, False, line_number)

def pseudo_assemble_add(line, tokens, line_number=None):
    # ADD <source> <destination>

    if len(tokens) != 3:
        error(line_number, line, f'invalid ADD syntax')
    
    source = tokens[1]
    destination = tokens[2]

    output_mnemonics = (
        'ALUFSET 0000000',
        f'ALUEVAL {source}',
        f'ALUSTORER {destination}',
    )

    return (itertools.chain(*(assemble(m, m.split()) for m in output_mnemonics)))


pseudo_instructions = {
    'LOADI': pseudo_assemble_loadi,
    'LOADI_UNSIGNED': pseudo_assemble_loadi_unsigned,
    'ADD': pseudo_assemble_add
}

for line in source_lines:
    line_number +=1
    line = line.strip()

    if line.startswith('/*'):
        multi_line_comment_block = True

    if line.startswith('//') or line.startswith('#') or multi_line_comment_block or not line:
        if line.endswith('*/'):
            multi_line_comment_block = False
        continue # Ignore comments and empty lines

    tokens = line.split()
    instruction = tokens[0].upper()
    
    if instruction in instructions:
        output += assemble(line, tokens, line_number)
    elif instruction in pseudo_instructions:
        print('\033[33mPSEUDO  ', line.ljust(20), '\033[0m', sep='\t')
        output += pseudo_instructions[instruction](line, tokens, line_number)
    else:
        error(line_number, line, f'"{instruction}" is not a valid instruction')
        exit(1)

    # output_instructions are already in hex

    # output += [format(int(i, 2), 'X') for i in output_instructions]

# generate output
output_file = open(output_file_name, 'w')
output_lines = ['v3.0 hex words addressed\n']

output_index = 0

for i in range(math.ceil(len(output) / 16)):
    line_number_str = format(i*16, 'x');
    output_line = line_number_str.zfill(5) + ':'
    
    for j in range(16):
        if output_index >= len(output):
            output_line += ' 000'
        else:
            output_line += ' ' + output[output_index].zfill(3)
            output_index += 1
    
    output_lines.append(output_line + '\n')


output_file.writelines(output_lines)
output_file.close()
print('done')