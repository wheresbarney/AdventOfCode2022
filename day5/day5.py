# https://adventofcode.com/2022/day/5

def parse(input):
    hold = [] # list of stacks
    moves = [] # list of tuple(count, origin, dest)

    for line in input:
        if '[' in line:
            for i in range((len(line)+1)//4):
                crate = line[i*4+1]
                if crate != ' ':
                    while len(hold) < i+1:
                        hold.append([])
                    hold[i].append(crate)
        elif 'move' in line:
            t = line.split(' ')
            moves.append((int(t[1]), int(t[3]), int(t[5])))

    [s.reverse() for s in hold]
    return hold, moves

def q1(input):
    hold, moves = parse(input)
    # print(f'{hold} {moves}')
    for count, src, dest in moves:
        # print(f'{count=} {src=} {dest=}')
        for i in range(count):
            hold[dest-1].append(hold[src-1].pop())
        # print(f'> {hold}')
    return ''.join([s[-1] for s in hold])

def q2(input):
    hold, moves = parse(input)
    for count, src, dest in moves:
        hold[dest-1].extend(hold[src-1][count * -1:])
        hold[src-1] = hold[src-1][:count * -1]
        # print(f'{hold}')
    return ''.join([s[-1] for s in hold])
