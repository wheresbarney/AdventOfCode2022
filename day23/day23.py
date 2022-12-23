# https://adventofcode.com/2022/day/23

from collections import defaultdict
from itertools import chain

# origin: bottom left
# list of tuples: (list of directions to check, destination)
RAW_DIRECTIONS = [
    ([(-1, 1), (0, 1), (1, 1)], (0, 1)), # N
    ([(-1, -1), (0, -1), (1, -1)], (0, -1)), # S
    ([(-1, -1), (-1, 0), (-1, 1)], (-1, 0)), # W
    ([(1, -1), (1, 0), (1, 1)], (1, 0)), # E
]

def q1(input):
    elfs = set()
    for y, line in enumerate(reversed(input)):
        elfs |= {(x, y) for x, c in enumerate(line) if c == "#" }

    for round in range(10):
        directions = [RAW_DIRECTIONS[(round + i) % 4] for i in range(4)]
        new_elfs = one_round(elfs, directions)

        if elfs == new_elfs:
            print(f"{round}: Complete: {elfs} is stable")
            break

        elfs = new_elfs

    x_min = min(x for x, _ in elfs)
    x_max = max(x for x, _ in elfs)
    y_min = min(y for _, y in elfs)
    y_max = max(y for _, y in elfs)

    print(f"Final arrangement at round {round} {(x_min, y_min)}:{(x_max, y_max)}")
    for y in range(y_max, y_min - 1, -1):
        print("".join(["#" if (x, y) in elfs else "." for x in range(x_min, x_max+1)]))

    return (x_max - x_min + 1) * (y_max - y_min + 1) - len(elfs)


def q2(input):
    elfs = set()
    for y, line in enumerate(reversed(input)):
        elfs |= {(x, y) for x, c in enumerate(line) if c == "#" }

    round = 0
    while True:
        directions = [RAW_DIRECTIONS[(round + i) % 4] for i in range(4)]
        new_elfs = one_round(elfs, directions)

        if elfs == new_elfs:
            print(f"{round}: Complete: {elfs} is stable")
            break

        elfs = new_elfs
        round += 1

        if round % 100 == 0:
            print (f"{round}")

    x_min = min(x for x, _ in elfs)
    x_max = max(x for x, _ in elfs)
    y_min = min(y for _, y in elfs)
    y_max = max(y for _, y in elfs)

    print(f"Final arrangement at round {round} {(x_min, y_min)}:{(x_max, y_max)}")
    for y in range(y_max, y_min - 1, -1):
        print("".join(["#" if (x, y) in elfs else "." for x in range(x_min, x_max+1)]))

    return round + 1


def one_round(elfs, directions):
    new_elfs = set()

    # 1. find the preferred new locations
    preferred_locations = defaultdict(int)
    movements = []
    for x, y in elfs:
        if any([any([(x + check[0], y + check[1]) in elfs for check in checks]) for checks, _ in directions]):
            for checks, move in directions:
                if all([(x + check[0], y + check[1]) not in elfs for check in checks]):
                    proposed = (x + move[0], y + move[1])
                    preferred_locations[proposed] += 1
                    movements.append(((x, y), proposed))
                    break
            if not movements or movements[-1][0] != (x, y):
                new_elfs.add((x, y))

        else:
            new_elfs.add((x, y))

    # 2. cancel any movements that lead to collision
    for current, preferred in movements:
        if preferred_locations[preferred] > 1:
            new_elfs.add(current)
        else:
            assert preferred_locations[preferred] == 1, "Found movement not in preferred set"
            new_elfs.add(preferred)

    assert len(elfs) == len(new_elfs), "elf count has changed"
    return new_elfs
