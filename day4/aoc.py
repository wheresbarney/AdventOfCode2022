# https://adventofcode.com/2022/day/4

def q1(input):
    fully_enclosed = 0

    for line in input:
        assignments = [[int(y) for y in x.split('-')] for x in line.split(',')]
        if assignments[0][0] >= assignments[1][0] and assignments[0][1] <= assignments[1][1]:
            fully_enclosed += 1
        elif assignments[1][0] >= assignments[0][0] and assignments[1][1] <= assignments[0][1]:
            fully_enclosed += 1

    return fully_enclosed


def q2(input):
    overlapped = 0

    for line in input:
        first, second = [[int(y) for y in x.split('-')] for x in line.split(',')]
        if first[0] >= second[0] and first[0] <= second[1]:
            overlapped += 1
        elif first[1] >= second[0] and first[1] <= second[1]:
            overlapped += 1
        elif second[0] >= first[0] and second[0] <= first[1]:
            overlapped += 1
        elif second[1] >= first[0] and second[1] <= first[1]:
            overlapped += 1

    return overlapped
