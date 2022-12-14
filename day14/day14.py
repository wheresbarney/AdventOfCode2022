# https://adventofcode.com/2022/day/14

def parse(input: [str]) -> set((int, int)):
    paths = [[(int(point.split(",")[0]), int(point.split(",")[1])) for point in path.split(" -> ")] for path in input]

    solids = set()
    for path in paths:
        current = path[0]
        for next in path[1:]:
            solids.add(current)

            if current[0] == next[0]:
                # vertical lines
                step = 1 if current[1] < next[1] else -1
                solids |= {(current[0], y) for y in range(current[1]+step, next[1], step)}
            elif current[1] == next[1]:
                # horiz lines
                step = 1 if current[0] < next[0] else -1
                solids |= {(x, current[1]) for x in range(current[0]+step, next[0], step)}
            else:
                raise AssertionError(f"line not horizontal or vertical: {current=} {next=}")

            current = next
        solids.add(next) # trailing point
    # print(f"{len(solids)}: {solids}")
    return solids

def q1(input: [str]) -> str:
    solids = parse(input)
    max_depth = max((point[1] for point in solids))
    grains = 0

    while True:
        s = next_sand_settles(solids, max_depth)
        if not s:
            return grains
        solids.add(s)
        grains += 1

def q2(input: [str]) -> str:
    solids = parse(input)
    max_depth = max((point[1] for point in solids))
    grains = 0

    while True:
        s = next_sand_settles_with_floor(solids, max_depth+2)
        if not s:
            return grains
        solids.add(s)
        grains += 1

ORIGIN = (500, 0)
FALLS = [(0, 1), (-1, 1), (1, 1)]

def next_sand_settles(solids: set((int, int)), max_depth: int) -> (int, int):
    s = ORIGIN
    while s[1] <= max_depth:
        for fall in FALLS:
            trial_loc = (s[0] + fall[0], s[1] + fall[1])
            if trial_loc not in solids:
                s = trial_loc
                break
        if s != trial_loc:
            # couldn't find a better place
            return s
    return None

def next_sand_settles_with_floor(solids: set((int, int)), floor: int) -> (int, int):
    s = ORIGIN
    if s in solids:
        return None

    while True:
        for fall in FALLS:
            trial_loc = (s[0] + fall[0], s[1] + fall[1])
            if trial_loc[1] == floor:
                return s

            if trial_loc not in solids:
                s = trial_loc
                break
        if s != trial_loc:
            # couldn't find a better place
            return s
    return None
