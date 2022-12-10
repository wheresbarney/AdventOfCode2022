#!/usr/bin/env python3.10
# https://adventofcode.com/2022

from sys import argv

# day func input

day = 'day' + argv[1]
src = f'./{day}/{day}.py'
function = argv[2]
input = f'./{day}/{argv[3]}.txt'

with open(src, 'rb') as f:
    code = compile(f.read(), src, 'exec')
exec(code)

with open(input, 'r') as f:
    data = [l.rstrip() for l in f]

if '1' in function:
    output = q1(data)
else:
    output = q2(data)
print(output)
