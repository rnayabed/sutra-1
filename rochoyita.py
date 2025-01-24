#!/bin/python
# rochoyita - simple assembler for sutra-1 
# supported target: Logisim compatible hex file

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


# TODO: use dataclass? or move all functions down here

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
    'ALUFSETR'   : Instruction(
        '10100100',
        (
            Operand(OperandType.SOURCE,         2),
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
    'AOP'      : Instruction(
        '10010100',
        (
            Operand(OperandType.DATA,           2),
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
    'ILOCKSET'  : Instruction(
        '101010000',
        (
            Operand(OperandType.DATA,           1),
        )
    ),
    'NOOP'      : Instruction('0000000000'),
    'HALT'      : Instruction('1111111111')
}
destination_registers = ('A', 'B', 'C', 'D', 'SP', 'IMR', 'MARL', 'MARH')
source_registers = ('A', 'B', 'C', 'D', 'SP', 'IMR', 'ISR')

def error(line_number, line, error):
    error_raw(
        f'ERROR{f' in line #{line_number}' if line_number is not None else ''}: "{line}"',
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
            error(line_number, line, f'invalid preprocessor use')

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
program_output = []
isr_output = []
ISR_ADDRESS = 0xff800       # TODO: move this to magic
label_addresses = {
    ':ISR': ISR_ADDRESS
}
label_unassembled_lines = []

# mnemonic -> hex
def assemble(line, tokens, line_number=None):
    instruction = instructions[tokens[0]]

    print('\033[32mASSEMBLE'.ljust(15), line.ljust(25), sep='\t', end='\t')

    if (len(tokens) - 1) != len(instruction.operands):
        error(line_number, line, f'operands mismatch. expected {len(instruction.operands)}, given {len(tokens) - 1}')

    output_instruction = instruction.op_code

    for i in range(len(tokens) - 1):

        operand_info = instruction.operands[i]

        token = tokens[i + 1]
        
        if operand_info.type == OperandType.DESTINATION:
            if token not in destination_registers:
                error(line_number, line, f'"{token}" is not a valid destination register')
            
            index = destination_registers.index(token)
            if index >= 2 ** operand_info.length:
                error(line_number, line, f'destination register "{token}" not allowed. it must be between {', '.join(destination_registers[i] for i in range(2 ** operand_info.length))}')

            output_instruction += format(index, 'b').zfill(operand_info.length)

        elif operand_info.type == OperandType.SOURCE:
            if token not in source_registers:
                error(line_number, line, f'"{token}" is not a valid source register')

            index = source_registers.index(token)
            if index >= 2 ** operand_info.length:
                error(line_number, line, f'source register "{token}" not allowed. it must be between {', '.join(source_registers[i] for i in range(2 ** operand_info.length))}')

            output_instruction += format(index, 'b').zfill(operand_info.length)
            
        elif operand_info.type == OperandType.DATA:
            if operand_info.length != len(token):
                error(line_number, line, f'operand "{token}" length mismatch. expected {operand_info.length}, given {len(token)}')

            if any(c not in '01' for c in token):
                error(line_number, line, f'"{token}" is not a valid binary number')

            output_instruction += token


    if len(output_instruction) != 10:
        error(line_number, line, f'resultant assembled instruction {output_instruction} does not match standard length')

    hex_ = format(int(output_instruction, 2), 'X').zfill(3)
    print(output_instruction, hex_ + '\033[0m', sep='\t')

    return hex_

# Helper funcs

def generate_binary(line_number, line, value_str, signed, bits):
    try:
        match value_str[0]:
            case 'h':
                base = 16
            case 'o':
                base = 8
            case 'b':
                base = 2
            case _:
                base = 10

        value_int = int(value_str if base == 10 else value_str[1:], base)

        if signed:
            max_value = 2**(bits - 1) - 1;
            min_value = - 2**(bits - 1);
            if value_int < min_value or value_int > max_value:
                error(line_number, line, f'invalid integer {value_str} - range must be between {min_value} and {max_value} (inclusive)')

            # remove '-' from value and convert into 2's compliment
            value = format(abs(value_int), 'b').zfill(bits)
            if value_int < 0:
                value = ''.join('1' if c == '0' else '0' for c in value)
                value = format(int(value, 2) + 1, 'b')
        else:
            max_value = 2**(bits) - 1;
            if value_int < 0 or value_int > max_value:
                error(line_number, line, f'invalid integer {value_str} - range must be between 0 and {max_value} (inclusive)')

            value = format(abs(value_int), 'b').zfill(bits)           

    except Exception as e:
        error(line_number, line, f'{value_str} is not a valid integer')
    
    return value

# Pseudo assemble: mnemonic -> another mnemonic

def pseudo_assemble_loadi(line, tokens, line_number, **kwargs):
    # LOADI <destination:2> <value>

    signed = tokens[0] == 'LOADI_SIGNED'
    
    destination = tokens[1]
    value_str = tokens[2]

    value = generate_binary(line_number, line, value_str, signed, bits=10)

    return (
        f'LOADIU {destination} {value[:5]}',
        f'LOADIL {destination} {value[5:]}'  
    )

# Math operations

'''
6 - OC
5 - N
4 - Cin
3 - BC
2 - BZ
1 - AC
0 - AZ

(A' + SOURCE)' = A - SOURCE     : AC, OC
(A  + SOURCE')' = SOURCE - A    : BC, OC
'''


def pseudo_assemble_alu_op(line, tokens, line_number, **kwargs):
    # ALUFSETO <option>

    option = tokens[1]

    match option:
        case 'ADD':
            o = '0000000'
        case 'SUB':
            o = '1000010'   # A - B
        case 'SUB_REV':
            o = '1001000'   # B - A
        case 'NAND':
            o = '0100000'
        case 'NOT':
            o = '0100011'   # B'
        case 'NOT_A':
            o = '0101100'   # A'
        case 'AND':
            o = '1100000'
        case _:
            error(line_number, line, f'invalid option {option}')

    return (f'ALUFSET {o}',)

# TODO: normalise method signatures?
def pseudo_assemble_loadmari(line, tokens, line_number, **kwargs):
    # LOADMARI <20 bit address or :label>

    address = tokens[1]
    if address.startswith(':'):
        return (
            f'>LOADIU A {address}_0_5',
            f'>LOADIL A {address}_5_10',
            'COPY A MARH',
            f'>LOADIU A {address}_10_15',
            f'>LOADIL A {address}_15_20',
            'COPY A MARL',
        )
    else:
        address_binary = generate_binary(line_number, line, tokens[1], signed=False, bits=20)

        '''
        MARH upper 0..4
        MARH lower 5..9
        MARL upper 10..14
        MARL lower 14..19
        '''
        return (
            f'LOADIU A {address_binary[:5]}',
            f'LOADIL A {address_binary[5:10]}',
            'COPY A MARH',
            f'LOADIU A {address_binary[10:15]}',
            f'LOADIL A {address_binary[15:]}',
            'COPY A MARL',
        )


# Stack ops
# TODO: add compiler protection

def pseudo_assemble_stack_push(line, tokens, line_number, **kwargs):
    # STACKPUSH <source>

    source = tokens[1]
        
    return (
        # update SP
        'ALUFSET 0000011',     # AZ, AC -> 111... + B = B - 1 (Decrement SP)
        'ALUEVAL SP',
        'ALUSTORER SP',

        # copy SP to MAR
        'COPY SP MARL',                     # lower bits
        'ALUFSET 0000111',                  # AZ, AC, BZ -> 111... + 0 = 111...(n-1) 
        'ALUEVAL A',                        # does not matter
        'ALUSTORER MARH',                   # upper bits

        # store value to Stack
        f'STORE {source}'
    )

def pseudo_assemble_stack_pop(line, tokens, line_number, **kwargs):
    # STACKPOP <destination>

    destination = tokens[1]

    output = [
        # copy SP to MAR
        'COPY SP MARL',                     # lower bits
        'ALUFSET 0000111',                  # AZ, AC, BZ -> 111... + 0 = 111...(n-1)
        'ALUEVAL A',                        # does not matter
        'ALUSTORER MARH',                   # upper bits
    ]

    if destination != 'A':
        output.append(f'COPY A {destination}')

    output += [
        # update SP
        f'LOADIU A 00000',      # temporarily use destination register for storing 1
        f'LOADIL A 00001',
        f'ALUFSET 0000000',                 # SP + 1
        'ALUEVAL SP',
        'ALUSTORER SP',
    ]

    if destination != 'A':
        output.append(f'COPY {destination} A')
    
    output.append(f'LOAD {destination}')

    return output

def pseudo_assemble_call(line, tokens, line_number, **kwargs):
    # CALL :label

    address = tokens[1]

    output = []

    # back up A, B, C, D, address upper, lower to stack

    # registers
    for r in 'ABCD':
        output += pseudo_assemble_stack_push(line, (None, r), line_number)

    # copy current address
    # output += pseudo_assemble_loadmari(line, (None, str(kwargs['current_ins_address'])), line_number)


    # copy current address
    current_ins_address = kwargs['current_ins_address']
    
    return_address=f':INTERNAL{current_ins_address}'

    '''
    MARH upper 0..4
    MARH lower 5..9
    MARL upper 10..14
    MARL lower 14..19
    '''
    output += [
        f'>LOADIU A {return_address}_0_5',
        f'>LOADIL A {return_address}_5_10',
        'COPY A MARH',
        f'>LOADIU B {return_address}_10_15',
        f'>LOADIL B {return_address}_15_20',
        'COPY B MARL',
    ]

    
    # upper and lower
    for r in 'AB':
        output += pseudo_assemble_stack_push(line, (None, r), line_number)

    output += pseudo_assemble_jump(line, ('J', address), line_number)

    label_addresses[return_address] = format(current_ins_address + len(output), 'b').zfill(20)

    # executed after RETURN
    # pop D, C, B, A
    for r in 'DCBA':
        output += pseudo_assemble_stack_pop(line, (None, r), line_number)
    
    return output

def pseudo_assemble_return(line, tokens, line_number, **kwargs):
    # RETURN

    output = []

    # pop lower to B and upper to A
    for r in 'BA':
        output += pseudo_assemble_stack_pop(line, (None, r), line_number)
    
    # copy address to MAR
    output += [
        'COPY A MARH',
        'COPY B MARL',
    ]
    
    # jump to address
    output.append('JUMP 00')
    
    return output

# TODO: setup base interrupts address


'''
JUMP MODES:
b1 b0   
0   0   unconditional
0   1   if zero
1   0   if negative
1   1   if carry 
'''



pseudo_jumps = {
    'J'     : '00',
    'JZ'    : '01',
    'JN'    : '10',
    'JC'    : '11',
}

def pseudo_assemble_jump(line, tokens, line_number, **kwargs):
    # <pseudo jump option> :label
    output = []

    address = tokens[1]

    if address.startswith(':'):
        output += [
            f'>LOADIU A {address}_0_5',
            f'>LOADIL A {address}_5_10',
            'COPY A MARH',
            f'>LOADIU A {address}_10_15',
            f'>LOADIL A {address}_15_20',
            'COPY A MARL',
        ]
    else:
        address_binary = generate_binary(line_number, line, tokens[1], signed=False, bits=20)

        '''
        MARH upper 0..4
        MARH lower 5..9
        MARL upper 10..14
        MARL lower 14..19
        '''
        output += [
            f'LOADIU A {address_binary[:5]}',
            f'LOADIL A {address_binary[5:10]}',
            'COPY A MARH',
            f'LOADIU A {address_binary[10:15]}',
            f'LOADIL A {address_binary[15:]}',
            'COPY A MARL',
        ]
    
    output.append(f'JUMP {pseudo_jumps[tokens[0]]}')

    return output

'''
Accumulator modes

S1  S2
B9  B10
I1  I0

0   0   Nothing
0   1   Shift right
1   0   Shift left
1   1   Load            divide clocks here based on Low/high bits

TODO: check if its worth without killing clock in A

'''

def pseudo_assemble_a_op(line, tokens, line_number, **kwargs):
    # AOPT

    option = tokens[1]

    match option:
        case 'SLEFT':
            o = '10'
        case 'SRIGHT':
            o = '01'
        case _:
            error(line_number, line, f'invalid option {option}')

    return (f'AOP {o}',)
    pass


# TODO: -1 from here and handle that in the checker
pseudo_instructions = {
    'LOADI'             : [pseudo_assemble_loadi,       2],
    'LOADI_SIGNED'      : [pseudo_assemble_loadi,       2],
    'ALUFSETO'          : [pseudo_assemble_alu_op,      1],
    'LOADMARI'          : [pseudo_assemble_loadmari,    1],
    'STACKPUSH'         : [pseudo_assemble_stack_push,  1],
    'STACKPOP'          : [pseudo_assemble_stack_pop,   1],
    'CALL'              : [pseudo_assemble_call,        1],
    'RETURN'            : [pseudo_assemble_return,      0],
    'AOPT'              : [pseudo_assemble_a_op,        1]
}

for pj in pseudo_jumps.keys():
    pseudo_instructions[pj] = [pseudo_assemble_jump,    1] 


isr_being_processed = False
output = program_output
for line in source_lines:
    line_number +=1
    line = line.strip()

    if line.startswith('/*'):
        multi_line_comment_block = True

    if line.startswith('//') or line.startswith('#') or multi_line_comment_block or not line:
        if line.endswith('*/'):
            multi_line_comment_block = False
        continue # Ignore comments and empty lines


    current_ins_address = len(output) + (ISR_ADDRESS if isr_being_processed else 0)

    if line.startswith(':'):
        if re.search(r'[\s_]', line):
            error(line_number, line, f'invalid label "{line}". It MUST not contain whitespace or "_"')

        if line[1:] == 'ISR':
            # move all further lines to ISR address
            isr_being_processed = True
            output = isr_output
            pass
        
        addr_binary = format(current_ins_address, 'b').zfill(20) # generate 20 bit address
        label_addresses[line] = addr_binary
        print(f'\033[35mLABEL'.ljust(15), line.ljust(10), str(current_ins_address).ljust(5), format(current_ins_address, 'X').zfill(4), '\033[0m', sep='\t')
        continue # Ignore label

    # Ignore trailing comments
    if '//' in line:
        line = line[:line.index('//')]

    tokens = line.split()
    instruction = tokens[0].upper()
    
    if instruction in instructions:
        output.append(assemble(line, tokens, line_number))
    elif instruction in pseudo_instructions:
        # TODO: use placeholders for colours
        # TODO: use constants for these magic numbers
        print('\033[33mPSEUDO'.ljust(15), line.ljust(20), '\033[0m', sep='\t')

        max_length = pseudo_instructions[instruction][1] + 1
        if len(tokens) != max_length:
            error(line_number, line, f'invalid {tokens[0]} syntax')

        output_mnemonics = pseudo_instructions[instruction][0](line, tokens, line_number, current_ins_address=current_ins_address)

        for m in output_mnemonics:
            if m[0] == '>':
                print('\033[32mASSEMBLE LATER'.ljust(15), m.ljust(20), '\033[0m', sep='\t')
                # TODO: refactor this to separate to save space?
                label_unassembled_lines.append((len(output), line_number, line, isr_being_processed))
                output.append(m)
            else:
                output.append(assemble(m, m.split(), None))

    else:
        error(line_number, line, f'"{instruction}" is not a valid instruction')
        exit(1)


if len(label_unassembled_lines) > 0:
    print('\n\033[36mResolve labels \033[0m')

# post process label_addresses
for l in label_unassembled_lines:
    line_number, original_line_number, original_line, is_isr = l

    output = isr_output if is_isr else program_output

    line = output[line_number][1:]  # remove leading '>'

    # f'>LOADIU A {address}_0_5',

    for token in line.split():
        if '_' in token:
            break
    
    label, start_index, stop_index = token.split('_')

    if label not in label_addresses:
        error(original_line_number, original_line, f'unable to resolve label {label}')

    line = line.replace(token, label_addresses[label][int(start_index):int(stop_index)])
    
    output[line_number] = assemble(line, line.split())

#TODO: handle case different instructions properly

# generate report
# guidelines
# total             00000 - FFFFF       1048576 words
# program           00000 - FF7FF       1046528 words
# ISR               FF800 - FFE0B          1548 words
# stack             FFE0C - FFFFF           500 words

PROGRAM_MAX_LENGTH = 1046528
ISR_MAX_LENGTH = 1548

print('\033[36m')
print('====Memory Layout====')
print('PROGRAM'.ljust(10), '00000', format(len(program_output) - 1, 'X').zfill(5), f'{len(program_output)} words', sep='\t')
if len(isr_output) > 0:
    print('ISR  '.ljust(10), format(ISR_ADDRESS, 'X').zfill(5), format(ISR_ADDRESS + len(program_output) - 1, 'X').zfill(5), f'{len(isr_output)} words', sep='\t')
print('=====================')
print('\033[0m')

if len(isr_output) > 0:
    ex = []
    if len(program_output) > PROGRAM_MAX_LENGTH:
        ex.append(f'program code exceeds max size and overlaps with ISR code space by {len(program_output) - PROGRAM_MAX_LENGTH} words')
    
    if len(isr_output) > ISR_MAX_LENGTH:
        ex.append(f'ISR code exceeds max size and overlaps with stack space by {len(isr_output) - ISR_MAX_LENGTH} words!')
    
    if ex: error_raw(ex)
elif len(isr_output) == 0 and len(program_output) > (PROGRAM_MAX_LENGTH + ISR_MAX_LENGTH):
    error_raw(f'program code exceeds max size and overlaps with stack space by {len(program_output) - (PROGRAM_MAX_LENGTH + ISR_MAX_LENGTH)} words')
    pass

# generate output
output_file = open(output_file_name, 'w')
output_lines = ['v3.0 hex words addressed\n']

def add_output_lines(output, base_address=0):
    output_index = 0
    for i in range(math.ceil(len(output) / 16)):
        line_number_str = format(base_address + (i * 16), 'X');
        output_line = line_number_str.zfill(5) + ':'
    
        for j in range(16):
            if output_index >= len(output):
                output_line += ' 000'
            else:
                output_line += ' ' + output[output_index]
                output_index += 1
            
        output_lines.append(output_line + '\n')

add_output_lines(program_output)
add_output_lines(isr_output, ISR_ADDRESS)

output_file.writelines(output_lines)
output_file.close()