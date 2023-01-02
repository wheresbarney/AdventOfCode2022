# https://adventofcode.com/2022/day/22

from re import compile

DIRS = [">", "v", "<", "^"]

def q1(input):
    tests()

    x, y, dir = solve(input[-1], input[:-2], next_pos)

    print(f"finished: {(x, y)}, {dir}")
    return 1000 * (y + 1) + 4 * (x + 1) + DIRS.index(dir)

def solve(code, board, next_pos):
    bounds = []
    walls = set()
    bounds_matcher = compile(r" *([\.|\#]+) *")
    for y, line in enumerate(board):
        span = bounds_matcher.match(line).span(1)
        bounds.append((span[0], span[1]-1)) # bounds are inclusive
        walls |= {(x, y) for x, c in enumerate(line) if c == "#"}
    # print(f"{bounds=}, {walls=}")

    dir = DIRS[0]
    pos_x = bounds[0][0]
    pos_y = 0

    m = compile(r"([L|R])")
    for instr in m.split(code):
        if instr == "L":
            new_dir_index = DIRS.index(dir) - 1
            if new_dir_index < 0:
                new_dir_index = 3
            dir = DIRS[new_dir_index]
        elif instr == "R":
                new_dir_index = DIRS.index(dir) + 1
                if new_dir_index > 3:
                    new_dir_index = 0
                dir = DIRS[new_dir_index]
        else:
            for i in range(int(instr)):
                next_x, next_y = next_pos(board, bounds, dir, pos_x, pos_y)
                # print(f"moving {dir} {(pos_x, pos_y)} => {(next_x, next_y)} [{i+1}/{int(instr)}]")
                if board[next_y][next_x] == "#":
                    break
                assert board[next_y][next_x] == ".", "fell off board"
                pos_x = next_x
                pos_y = next_y

    return pos_x, pos_y, dir

def next_pos_flat(board, bounds, dir, x, y):
    assert board[y][x] in ["#", "."], "Fell off board!"

    if dir == ">":
        if x < bounds[y][1]:
            return x + 1, y
        return bounds[y][0], y
    if dir == "<":
        if x > bounds[y][0]:
            return x - 1, y
        return bounds[y][1], y
    if dir == "^":
        if y > 0 and bounds[y-1][0] <= x <= bounds[y-1][1]:
            return x, y - 1
        for i in range(len(bounds) - 1, -1, -1):
            if bounds[i][0] <= x <= bounds[i][1]:
                return x, i
    assert dir == "v", "unexpected direction"
    if y < (len(bounds) - 1) and (bounds[y+1][0] <= x <= bounds[y+1][1]):
        return x, y + 1
    for i in range(len(bounds)):
        if bounds[i][0] <= x <= bounds[i][1]:
            return x, i
    raise AssertionError("Failed to find next position")

def tests():
    def test(label, code, board, exp):
        act = solve(code, board)
        assert act == exp, f"{label}: {exp=} {act=}"

    two_by_two_with_leading_trailing = [
        " .. ",
        " .. ",
    ]
    complex_grid = [
        "  .#",
        " .. ",
        "..  ",
        "#.  ",
    ]

    test("simple", "1R1", two_by_two_with_leading_trailing, (2, 1, "v"))
    test("wrap_right", "3", two_by_two_with_leading_trailing, (2, 0, ">"))
    test("wrap_left", "0L0L1", two_by_two_with_leading_trailing, (2, 0, "<"))
    test("wrap_up", "0R0R0R1", two_by_two_with_leading_trailing, (1, 1, "^"))
    test("wrap_down", "0R2", two_by_two_with_leading_trailing, (1, 0, "v"))
    test("double_digits", "11L13", two_by_two_with_leading_trailing, (2, 1, "^"))
    test("complex", "1R0R0R0R2L1R3L1R5R2L1L0L2L5L0", complex_grid, (0, 2, ">"))
