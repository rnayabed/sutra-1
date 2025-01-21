#!/bin/python

# /*
# Screen commands:
# select row and column   01<row bank:2><column index:6>
# row data                10<data:8>
# load buffer             1100000000
# */

import argparse

# handle args
parser = argparse.ArgumentParser(
    prog='shilpo',
    description='Simple pixel drawer from the Sutra-1 System',
    epilog='Copyright (C) 2025 Debayan "rnayabed" Sutradhar'
)

parser.add_argument('-o', '--output')
parser.add_argument('input')
args = parser.parse_args()

input_file_name = args.input
output_file_name = args.output if args.output is not None else input_file_name + '.sutra-1'

with open(input_file_name, 'r') as f:
    # art = f.readlines()
    art = f.read().strip()

print(art)

def get_pixel(row, col):
    return art[col + (65 * row)] == '#'
    # return art[row][col] == '#'

output = ['LOADI C b1100000000']

reg_values={}
def set_reg(reg, value):
    if reg not in reg_values or reg_values[reg][:5] != value[:5]:
        output.append(f'LOADIU {reg} {value[:5]}')
    if reg not in reg_values or reg_values[reg][5:10] != value[5:10]:
        output.append(f'LOADIL {reg} {value[5:10]}')

    reg_values[reg] = value

    # output.append(f'LOADI {reg} b{value}')
    output.append(f'OUT {reg}')
    print(f'reg {reg}, value {value}')

# A = row bank & col index
# B = row data
# C = load buffer command


for c in range(64):
    for rb in range(4):
        o = ''
        empty = True
        for i in range(8):
            row = (((3 - rb)) * 8) + i
            # 24,25,26,27, 28,29,30,31 (rb = 0)
            # 16,17,18,19, 20,21,22,23 (rb = 1)
            # 8,9,10,11,   12,13,14,15 (rb = 2)
            # 0,1,2,3,     4,5,6,7
            if get_pixel(row, c):
                o += '1'
                empty = False
            else:
                o += '0' 
        
        if not empty:
            # select row and column   01<row bank:2><column index:6>
            print(f'row bank {rb}, column {c}')
            set_reg('A', f'01{format(rb, 'b').zfill(2)}{format(c, 'b').zfill(6)}')
            
            # row data                10<data:8>
            set_reg('B', '10' + o)

            output.append('OUT C')

output.append('HALT')

with open(output_file_name, 'w') as f:
    for l in output:
        f.write(l + '\n')