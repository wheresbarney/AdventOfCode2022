# https://adventofcode.com/2022/day/17

from dataclasses import dataclass, field
from itertools import cycle
from functools import cache

@dataclass(frozen=True)
class Rock:
    name: str
    offsets: [(int, int)] = field(repr=False)

    # @cache
    def width(self):
        return max([o[0] for o in self.offsets])

# origin is bottom left corner of bounding rectangle
ROCKS = [
    Rock("—", [(0, 0), (1, 0), (2, 0), (3, 0)]),
    Rock("+", [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
    Rock("⌟", [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    Rock("|", [(0, 0), (0, 1), (0, 2), (0, 3)]),
    Rock("#", [(0, 0), (1, 0), (0, 1), (1, 1)]),
    ]

LEFT_WALL = 0 # x can't go below 0
RIGHT_WALL = 6 # x can't go above 6

def q1(input):
    return solve(input, 2022)

def q2(input):
    return solve(input, 1_000_000_000_000)

def solve(input, rock_target):
    jets = cycle(enumerate(input[0]))
    rocks = cycle(enumerate(ROCKS))
    stack = set()
    highest = 0 # floor
    total_rocks = 0

    rock_num, rock = next(rocks)
    origin = (2,3)

    pattern_identified = False
    cache = {} # {(last_20_rows, rock, jet): (rock_count, max_height)}
    extra_height_to_add = 0
    # heights = [0]

    while total_rocks < rock_target:
        # blow with the next jet
        jet_num, jet = next(jets)
        jetx = 1 if jet == ">" else -1
        impeded = origin[0] + jetx < LEFT_WALL or origin[0] + rock.width() + jetx > RIGHT_WALL
        if not impeded and origin[1] <= highest:
            for offset in rock.offsets:
                new = (origin[0] + offset[0] + jetx, origin[1] + offset[1])
                if new in stack:
                    impeded = True
                    break
        if not impeded:
            origin = (origin[0] + jetx, origin[1])

        # drop if possible
        impeded = False
        if origin[1] <= highest + 1:
            for offset in rock.offsets:
                new = (origin[0] + offset[0], origin[1] + offset[1] - 1)
                if new[1] < 0 or new in stack:
                    impeded = True
                    break
        if not impeded:
            # drop it
            origin = (origin[0], origin[1] - 1)
            # print(f"{rocks}: Dropping {rock} to {origin}")
        else:
            # it can go no further; it's landed
            for offset in rock.offsets:
                current = (origin[0] + offset[0], origin[1] + offset[1])
                stack.add(current)
                highest = max(highest, current[1])
            # heights.append(highest)

            if total_rocks % 1000 == 0:
                print(f"{total_rocks}: Landed {rock} {origin} {highest=}")

            total_rocks += 1
            rock_num, rock = next(rocks)
            origin = (2, highest + 4)

            if not pattern_identified:
                cache_key = get_key(stack, highest, rock_num, jet_num)
                if cache_key in cache:
                    pattern_identified = True
                    prev_total_rocks, prev_highest = cache[cache_key]
                    stride = total_rocks - prev_total_rocks
                    cycles = (rock_target - total_rocks) // stride

                    # debugging sample case only
                    # cycles -= 1

                    # if we're going to run the remaining loops...
                    extra_height_to_add = (highest - prev_highest) * cycles
                    prev_rock_target = rock_target
                    rock_target -= cycles * stride # fast-forward
                    print(f"{total_rocks}: skipping {cycles} x {stride} rocks ({extra_height_to_add=}) reducing cycles from {prev_rock_target} to {rock_target}")

                    # or can we look up the height of the remaining rocks?
                    # remainder = (rock_target - total_rocks) % stride
                    # remainder = rock_target - (cycles * stride) - total_rocks

                    # assert prev_highest == heights[prev_total_rocks], f"mismatch {prev_highest=} {heights[prev_total_rocks]=}"
                    # return sum([
                    #     highest, # preamble
                    #     (highest - prev_highest) * cycles, # repeating pattern
                    #     heights[prev_total_rocks+remainder] - heights[prev_total_rocks], # trailing
                    #     1, # zero-based to one-based counting
                    # ])
                else:
                    cache[cache_key] = (total_rocks, highest)

    # for y in range(highest, -1, -1):
    #     print("".join(["#" if stack[x][y] else "." for x in range(RIGHT_WALL + 1)]))
    return highest + extra_height_to_add + 1

def get_key(stack, highest, rock_counter, jet_counter):
    top_n_rows = "".join(
        [str((x, y) in stack) for x in range(RIGHT_WALL + 1) for y in range(highest, highest - 100)]
    )
    return (top_n_rows, rock_counter, jet_counter)
