# https://adventofcode.com/2022/day/3

from sys import argv
from string import ascii_letters

def q1(input):
    total = 0

    for rucksack in input:
        split = int(len(rucksack)/2)
        first_compartment = set(rucksack[:split])
        overlap = set(rucksack[:split]) & set(rucksack[split:])
        total += ascii_letters.index(overlap.pop()) + 1

    return total


def q2(input):
    total = 0
    i = 0
    while i < len(input):
        s = set(input[i])
        s &= set(input[i+1]) & set(input[i+2])
        # print(f'team {i}, common item {s}')
        total += ascii_letters.index(s.pop()) + 1
        i += 3
    return total
