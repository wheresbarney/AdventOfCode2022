#!/usr/bin/env python3.8
# https://adventofcode.com/2022

from sys import argv

subdir = argv[1]
input = './' + subdir + '/' + argv[3]
function = argv[2]
src = subdir + '/aoc.py'

with open(src, 'rb') as f:
    code = compile(f.read(), src, 'exec')
exec(code)

with open(input, 'r') as f:
    data = [l.strip() for l in f]
    if '1' in function:
        output = q1(data)
    else:
        output = q2(data)
    print(output)
