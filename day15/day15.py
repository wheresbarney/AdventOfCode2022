# https://adventofcode.com/2022/day/15

from re import compile

def q1(input: [str]) -> str:
    target_row = 10 if len(input) == 14 else 2000000

    m = compile("(-?\d+)")
    sensor_beacons = [[int(n) for n in m.findall(line)] for line in input]

    explored_spaces = set()
    for sx, sy, bx, by in sensor_beacons:
        explored_spaces |= explored_space_on_row(sx, sy, bx, by, target_row)

    # print(sorted(explored_spaces))
    return len(explored_spaces)

def explored_space_on_row(sx: int, sy: int, bx: int, by: int, row: int, bounds: int = None) -> {int}:
    explored = set()

    beacon_sensor_distance = abs(sx - bx) + abs(sy - by)
    sensor_target_distance = abs(sy - row)

    # print(f"beacon={(bx, by)} sensor={(sx, sy)} b:s={beacon_sensor_distance} s:row={sensor_target_distance}")
    for i in range(beacon_sensor_distance - sensor_target_distance + 1):
        # print(f"  adding {sx+i}, {sx-i}")
        if by == row and sx+i == bx:
            # don't add beacon to set
            pass
        elif bounds and (sx+i < 0 or sx+i >= bounds):
            # don't track outside of bounded box
            pass
        else:
            explored.add(sx + i)

        if by == row and sx-i == bx:
            # don't add beacon to set
            pass
        elif bounds and (sx-i < 0 or sx-i >= bounds):
            # don't track outside of bounded box
            pass
        else:
            explored.add(sx - i)

    return explored

def explored_range(bounds: int, row: int, sx: int, sy: int, bx: int, by: int) -> [[int]]:
    beacon_sensor_distance = abs(sx - bx) + abs(sy - by)
    sensor_target_distance = abs(sy - row)
    overflow = beacon_sensor_distance - sensor_target_distance
    if overflow < 0:
        return None

    floor, ceiling = sorted([max(0, sx - overflow), min(bounds, sx + overflow + 1)])
    # print(f"{row}: beacon={(bx, by)} sensor={(sx, sy)} => {floor}/{ceiling} [b:s={beacon_sensor_distance} s:row={sensor_target_distance} play={overflow}]")
    return (floor, ceiling)

def q2(input: [str]) -> str:
    bounds = 20 if len(input) == 14 else 4_000_000

    m = compile("(-?\d+)")
    sensor_beacons = [[int(n) for n in m.findall(line)] for line in input]

    for y in range(bounds):
        if y % 100000 == 0:
            print(f"testing row {y}")
        explored = [explored_range(bounds, y, *sb) for sb in sensor_beacons]
        explored = [e for e in explored if e]
        explored.sort()
        if explored[0][0] != 0:
            return f"Found it on x=0,{y=}: {explored}"
            return 0 * 4_000_000 + y
        ceil = explored[0][1]
        for rng in explored[1:]:
            if rng[0] > ceil:
                print(f"Found it on x={ceil},{y=}: {rng}")
                return ceil * 4_000_000 + y
            ceil = max(ceil, rng[1])
