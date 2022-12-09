# https://adventofcode.com/2022/day/9

def q1(input):
    moves = [(j[0], int(j[1])) for j in [i.split() for i in input]]

    h = (0,0)
    t = (0,0)
    visited = {t}

    for move in moves:
        for _ in range(move[1]):
            h = move_knot(h, move[0])
            t = move_tail(h, t)
            visited.add(t)

    return len(visited)

def q2(input):
    moves = [(j[0], int(j[1])) for j in [i.split() for i in input]]

    knots = [(0,0)] * 10
    visited = {knots[-1]}

    for move in moves:
        for _ in range(move[1]):
            knots[0] = move_knot(knots[0], move[0])
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i-1], knots[i])
            visited.add(knots[-1])

    return len(visited)

move_map = {'R': (0, 1), 'L': (0, -1), 'U': (1, 0), 'D': (-1, 0)}
def move_knot(pos, dir):
    move = move_map[dir]
    return (pos[0] + move[0], pos[1] + move[1])

def move_tail(h, t):
    moves = []
    if abs(t[0] - h[0]) <= 1 and abs(t[1] - h[1]) <= 1:
        pass
    else:
        if t[0] != h[0]:
            moves.append('U' if h[0] > t[0] else 'D')
        if t[1] != h[1]:
            moves.append('R' if h[1] > t[1] else 'L')
    # print(f'{h=} {t=} {moves=}')
    for move in moves:
        t = move_knot(t, move)
    # print(f' => {h=} {t=}')
    return t
