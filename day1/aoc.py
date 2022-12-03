#!/usr/bin/env python3.8
# https://adventofcode.com/2022/day/1

from sys import argv

def parse(input):
    elves = [[]]
    for line in input:
        if not line:
            elves.append([])
            continue
        elves[-1].append(int(line))
    return elves


def q1(input):
    return max([sum(elf) for elf in parse(input)])


def q2(input):
    return sum(sorted([sum(elf) for elf in parse(input)])[-3:])


with open(argv[1], 'r') as f:
    print(q2([l.strip() for l in f]))
