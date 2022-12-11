#!/usr/bin/env python3.10
# https://adventofcode.com/2022/day/11

from __future__ import annotations
from collections import deque
from typing import Callable
from functools import partial
from operator import add, mul, pow

class Monkey:
    def __init__(self,
                 items: [int],
                 worry_function: Callable[int, int],
                 divisible: int,
                 pass_if_true: int,
                 pass_if_false: int):
        self.items = deque(items)
        self.worry_function = worry_function
        self.divisible = divisible
        self.pass_if_true = pass_if_true
        self.pass_if_false = pass_if_false
        self.inspected = 0
        self.item_modulos = deque()


    def __repr__(self):
        # return f"Monkey(items:{self.items} inspected={self.inspected}"
        return f"Monkey(inspected={self.inspected} mods={self.item_modulos})"

    def play_with_items_with_worry_reduction(self, monkeys: [Monkey]) -> None:
        while self.items:
            orig_item = self.items.popleft()
            new_item = self.worry_function(orig_item) // 3
            next = self.pass_if_true if new_item % self.divisible == 0 else self.pass_if_false
            monkeys[next].items.append(new_item)
            self.inspected += 1
            # print(f"item {orig_item} => {new_item}, thrown to {next}")

    def set_divisors_to_track(self, divisors: set(int)) -> None:
        for item in self.items:
            map = {}
            for divisor in divisors:
                map[divisor] = item % divisor
            self.item_modulos.append(map)

    def play_with_items_without_worry_reduction(self, monkeys: [Monkey]) -> None:
        while self.item_modulos:
            orig_item = self.item_modulos.popleft()
            new_item = {}
            for c, d in orig_item.items():
                val = self.worry_function(d)
                # print(f"  {self.divisible} working on {orig_item} ({c}, {d}, {val})")
                new_item[c] = val % c
            test_divisor = new_item[self.divisible] == 0
            next = self.pass_if_true if test_divisor else self.pass_if_false
            monkeys[next].item_modulos.append(new_item)
            self.inspected += 1
            # print(f"item {orig_item} => {new_item}, thrown to {next}")


def parse(input: str) -> [Monkey]:
    monkeys = []

    for line in input:
        match line.replace(",", "").replace(":", "").split():
            case "Monkey", _:
                items = worry_function = divisible = \
                    pass_if_true = pass_if_false = None
            case "Starting", "items", *capture:
                items = [int(s) for s in capture]
            case "Operation", _, _, var1, op, var2:
                match var1, op, var2:
                    case "old", "+", "old":
                        worry_function = partial(mul, 2)
                    case "old", "*", "old":
                        worry_function = partial(lambda p, x: pow(x, p), 2)
                    case "old", "+", v:
                        worry_function = partial(add, int(v))
                    case "old", "*", v2:
                        worry_function = partial(mul, int(v2))
            case "Test", "divisible", "by", n:
                divisible = int(n)
            case "If", "true", _, _, _, m:
                pass_if_true = int(m)
            case "If", "false", _, _, _, m2:
                pass_if_false = int(m2)
                monkeys.append(
                    Monkey(items, worry_function, divisible, pass_if_true, pass_if_false))

    return monkeys

def q1(input: str) -> int:
    monkeys = parse(input)
    # print(monkeys)
    for round in range(20):
        for i, monkey in enumerate(monkeys):
            # print(f"\nRound {round}, monkey {i}")
            monkey.play_with_items_with_worry_reduction(monkeys)

    inspections = [m.inspected for m in monkeys]
    inspections.sort()
    inspections.reverse()
    return inspections[0] * inspections[1]

def q2(input: str) -> int:
    monkeys = parse(input)
    divisors = {monkey.divisible for monkey in monkeys}
    for m in monkeys: m.set_divisors_to_track(divisors)

    for round in range(10000):
    # for round in range(2):
        for i, monkey in enumerate(monkeys):
            # print(f"\nRound {round}, monkey {i}")
            monkey.play_with_items_without_worry_reduction(monkeys)
        if round % 100 == 0:
            print(f"Round {round} {monkeys}")
        # for i, m in enumerate(monkeys):
        #     print(f"  {i}: {monkey}")

    inspections = [m.inspected for m in monkeys]
    inspections.sort()
    inspections.reverse()
    return inspections[0] * inspections[1]
