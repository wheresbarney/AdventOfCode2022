# https://adventofcode.com/2022/day/13

from functools import cmp_to_key
from re import compile

DIGITS = compile("\d+")

def q1(input: [str]) -> str:
    sum_matching_indices = 0
    pairs = [(input[i], input[i+1]) for i in range(0, len(input), 3)]

    for i, (left, right) in enumerate(pairs):
        if correctly_ordered(left, right):
            # print(f"pair {i+1} is correctly ordered")
            sum_matching_indices += i + 1
        # else:
        #     print(f"pair {i+1} is NOT correctly ordered")

    return sum_matching_indices

def q2(input: [str]) -> int:
    divider_packets = ["[[2]]", "[[6]]"]

    packets = [p for p in input if p]
    packets.extend(divider_packets)

    packets = sorted(packets, key=cmp_to_key(lambda l, r: -1 if correctly_ordered(l, r) else 1))
    # print("\n".join(packets))

    return (packets.index(divider_packets[0]) + 1) * (packets.index(divider_packets[1]) + 1)



def correctly_ordered(left: str, right: str, indent: int = 1) -> bool:
    # print(f"{' ' * indent}comparing {left} <> {right}")

    left = left.lstrip(",")
    right = right.lstrip(",")

    if left[0] == "[" and right[0] == "[":
        # recurse, stripping leading bracket
        return correctly_ordered(left[1:], right[1:], indent + 1)

    if left[0].isdecimal() and right[0].isdecimal():
        left_match = DIGITS.match(left)
        right_match = DIGITS.match(right)
        l = int(left_match.group())
        r = int(right_match.group())

        if l > r:
            return False
        if l < r:
            return True
        return correctly_ordered(left[left_match.end():], right[right_match.end():], indent)

    elif left[0] == "]" and right[0] == "]":
        # recurse, stripping leading bracket
        return correctly_ordered(left[1:], right[1:], indent + 1)
    elif left[0] == "]" and right[0] != "]":
        return True
    elif left[0] != "]" and right[0] == "]":
        # print(f"{' ' * indent} Failing because right array {right} exhausted before left {left}")
        return False

    elif left[0].isdecimal() != right[0].isdecimal():
        if left[0].isdecimal():
            m = DIGITS.match(left)
            return correctly_ordered(f"[{m.group()}],{left[m.end():]}", right, indent+1)
        else:
            m = DIGITS.match(right)
            return correctly_ordered(left, f"[{m.group()}],{right[m.end():]}", indent+1)

    assert False, f"unexpected fallthrough {left=} {right=}"
