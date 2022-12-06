# https://adventofcode.com/2022/day/6

def q1(input):
    for line in input:
        start = 0
        for i in range(4, len(line)):
            unique = set(line[i-4:i])
            # print(f'  {i=} {line[i-4:i]} -> {unique}')
            if len(unique) == 4:
                start = i
                print(f'{start=} for {line}')
                break

def q2(input):
    for line in input:
        start = 0
        for i in range(14, len(line)):
            unique = set(line[i-14:i])
            if len(unique) == 14:
                start = i
                print(f'{start=} for {line[:10]}...')
                break
