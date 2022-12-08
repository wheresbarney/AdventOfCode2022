# https://adventofcode.com/2022/day/8

def visible(trees, outer_range, inner_range, ignore, row_then_col = True):
    visible = 0
    for i in outer_range:
        max = -1
        for j in inner_range:
            r = i if row_then_col else j
            c = j if row_then_col else i

            tree = trees[r][c]

            if tree > max:
                max = tree
                if (r, c) not in ignore:
                    visible += 1
                    ignore.add((r, c))

            if max == 9:
                break

    return visible

def q1(input):
    trees = [[int(t) for t in row] for row in input]
    rows = len(trees)
    cols = len(trees[0])

    ignore = set()

    # visible from left
    visible = visible(trees, range(rows), range(cols), ignore)

    # visible from right
    visible += visible(trees, range(rows), range(cols-1, -1, -1), ignore)

    # visible from top
    visible += visible(trees, range(cols), range(rows), ignore, False)

    # visible from bottom
    visible += visible(trees, range(cols), range(rows-1, -1, -1), ignore, False)

    return visible

def count_scenic(trees, max, fixed, range, left_right = True):
    count = 0
    for r in range:
        tree = trees[fixed][r] if left_right else trees[r][fixed]
        # print(f'    {[fixed, r]} ({left_right=}): {tree} ({max=}')
        count += 1
        if tree >= max:
            break
    return count

def q2(input):
    trees = [[int(t) for t in row] for row in input]
    rows = len(trees)
    cols = len(trees[0])

    max_scenic = 0

    for row in range(rows):
        for col in range(cols):
            tree = trees[row][col]
            r = count_scenic(trees, tree, row, range(col+1, cols))
            if r == 0: continue
            l = count_scenic(trees, tree, row, range(col-1, -1, -1))
            if l == 0: continue
            d = count_scenic(trees, tree, col, range(row+1, rows), False)
            if d == 0: continue
            u = count_scenic(trees, tree, col, range(row-1, -1, -1), False)

            scenic = l * r * u * d
            # print(f'{[row, col]} ({tree}): {scenic} ({r=} {l=} {d=} {u=})')

            max_scenic = max(max_scenic, scenic)
    return max_scenic
