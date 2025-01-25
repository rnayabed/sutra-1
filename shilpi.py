#!/bin/python
# shilpi - Simple pixel drawer for Sutra-1
# SPDX-License-Identifier: GPL-3.0-only

'''
Display commands:
select row and column   01<row bank:2><column index:6>
row data                10<data:8>
load buffer             1100000000
'''

import argparse, math, os
from pathlib import Path

VERSION = 1.0

def error_raw(*text):
    print('\033[1;4;7;31m') # red with blue, underline, inverted text
    print('\n'.join(text))
    print('\033[0m')
    exit(1)

def generate_art_from_text(text):
    chars = {
        'A': '''
........
.######.
.#....#.
.######.
.#....#.
.#....#.
.#....#.
........
''',
        'B': '''
........
.######.
.#....#.
.#...#..
.#####..
.#....#.
.######.
........
''',
        'C': '''
........
.######.
.#......
.#......
.#......
.#......
.######.
........
''',
        'D': '''
........
.####...
.#...#..
.#....#.
.#....#.
.#...#..
.####...
........
''',
        'E': '''
........
.######.
.#......
.######.
.#......
.#......
.######.
........
''',
        'F': '''
........
.######.
.#......
.#......
.######.
.#......
.#......
........
''',
        'G': '''
........
.######.
.#......
.#..##..
.#....#.
.#....#.
.######.
........
''',
        'H': '''
........
.#....#.
.#....#.
.######.
.#....#.
.#....#.
.#....#.
........
''',
        'I': '''
........
.######.
...#....
...#....
...#....
...#....
.######.
........
''',
        'J': '''
........
.######.
....#...
....#...
....#...
.#..#...
..###...
........
''',
        'K': '''
........
.#...#..
.#..#...
.###....
.#.#....
.#..#...
.#...#..
........
''',
        'L': '''
........
.#......
.#......
.#......
.#......
.#......
.######.
........
''',
        'M': '''
........
.##..##.
.#.##.#.
.#.#..#.
.#....#.
.#....#.
.#....#.
........
''',
        'N': '''
........
.##...#.
.#.#..#.
.#.#..#.
.#..#.#.
.#...##.
.#...##.
........
''',
        'O': '''
........
.######.
.#....#.
.#....#.
.#....#.
.#....#.
.######.
........
''',
        'P': '''
........
.######.
.#....#.
.######.
.#......
.#......
.#......
........
''',
        'Q': '''
........
.####...
.#...#..
.#....#.
.#...##.
.######.
......#.
........
''',
        'R': '''
........
.#####..
.#....#.
.#####..
.##.....
.#.#....
.#..##..
........
''',
        'S': '''
........
.######.
..#.....
...#....
....#...
.....#..
.######.
........
''',
        'T': '''
........
.######.
...#....
...#....
...#....
...#....
...#....
........
''',
        'U': '''
........
.#....#.
.#....#.
.#....#.
.#....#.
.#....#.
.######.
........
''',
        'V': '''
........
.#....#.
.#...#..
.#..#...
.#.#....
.##.....
.#......
........
''',
        'W': '''
........
.#....#.
.#....#.
.#....#.
.#.#..#.
.#.#..#.
.######.
........
''',
        'X': '''
........
.#...#..
..#.#...
...#....
...#....
..#.#...
.#...#..
........
''',
        'Y': '''
........
.#....#.
.#....#.
.######.
...#....
...#....
...#....
........
''',
        'Z': '''
........
.######.
.....##.
....#...
...#....
.##.....
.######.
........
''',
        '0': '''
........
.######.
.#....#.
.#....#.
.#....#.
.#....#.
.######.
........
''',
        '1': '''
........
....#...
..###...
....#...
....#...
....#...
.######.
........
''',
        '2': '''
........
.######.
......#.
.######.
.#......
.#......
.######.
........
''',
        '3': '''
........
.######.
......#.
.######.
......#.
......#.
.######.
........
''',
        '4': '''
........
.#....#.
.#....#.
.######.
......#.
......#.
......#.
........
''',
        '5': '''
........
.######.
.#......
.######.
......#.
......#.
.######.
........
''',
        '6': '''
........
.######.
.#......
.######.
.#....#.
.#....#.
.######.
........
''',
        '7': '''
........
.######.
......#.
......#.
......#.
......#.
......#.
........
''',
        '8': '''
........
.######.
.#....#.
.######.
.#....#.
.#....#.
.######.
........
''',
        '9': '''
........
.######.
.#....#.
.######.
......#.
......#.
......#.
........
''',
        '0': '''
........
.######.
.#....#.
.#....#.
.#....#.
.#....#.
.######.
........
''',
        ' ': '''
........
........
........
........
........
........
........
........
'''
    }

    # each character occupies 8 rows and 8 columns
    # col = 7
    # row = 7
    # print(chars[' '].strip()[col + (9 * row)])
    # exit()

    text_index = 0

    # col_units = math.ceil(len(text) / 8)        # 9
    
    # row_units = math.ceil(col_units / (64/8))   # 9/8 = 2

    text = text.upper()

    MAX_LEN = 8*4
    if len(text) > MAX_LEN:
        error_raw(f'Text too long! Max permitted length is {MAX_LEN}')

    rows = []
    for i in range(0, len(text), 8):
        e = i+8
        rows.append(text[i:e] if e < len(text) else text[i:].ljust(8))

    rows = rows[:4]

    if len(rows) < 4:
        for i in range(4 - len(rows)):
            rows.append(' '*8)

    art = ''
    for row_text in rows:
        for row in range(8):
            for char in row_text:
                for col in range(8):
                    if char not in chars:
                        error_raw(f'character "{char}" in input text is not supported.')
                    art += chars[char].strip()[col + (9 * row)]
            art+='\n'
    
    return art



# handle args
parser = argparse.ArgumentParser(
    prog='shilpi',
    description='Simple pixel drawer from the Sutra-1 System',
    epilog='Copyright (C) 2025 Debayan "rnayabed" Sutradhar'
)

input_group = parser.add_mutually_exclusive_group()
input_group.add_argument('-v', '--version', action='store_true', help='Version and copyright information')
input_group.add_argument('input', nargs='?', help='Input text or file')
parser.add_argument('-o', '--output')
parser.add_argument('-t', '--text', action='store_true')
args = parser.parse_args()

if args.version:
    print(f'''shilpi Version {VERSION}
Copyright (C) 2025 Debayan Sutradhar

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. ''')
    exit()

if args.text:
    art = generate_art_from_text(args.input)
    output_file_name = args.output if args.output else 'art.S'
    print(art)
else:
    input_file_name = args.input

    output_file_name = args.output if args.output else f'{Path.cwd()}{os.sep}art.S'

    with open(input_file_name, 'r') as f:
        # art = f.readlines()
        art = f.read().strip()

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
    # print(f'reg {reg}, value {value}')

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
            # print(f'row bank {rb}, column {c}')
            set_reg('A', f'01{format(rb, 'b').zfill(2)}{format(c, 'b').zfill(6)}')
            
            # row data                10<data:8>
            set_reg('B', '10' + o)

            output.append('OUT C')

output.append('HALT')

with open(output_file_name, 'w') as f:
    for l in output:
        f.write(l + '\n')