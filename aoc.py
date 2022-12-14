#!/usr/bin/env python3.10
# https://adventofcode.com/2022

from sys import argv
from time import perf_counter

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

t1 = perf_counter()
if '1' in function:
    output = q1(data)
else:
    output = q2(data)
t2 = perf_counter()

print(output)
print(f"Execution time: {t2 - t1:0.4f} seconds")
