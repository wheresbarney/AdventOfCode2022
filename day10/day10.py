# https://adventofcode.com/2022/day/10

class Cpu:
    def __init__(self):
        self.clock = 1
        self.x = 1
        self.sum_signal_strength = 0

    def tick(self):
        h = (self.clock - 1) % 40
        if self.x >= h-1 and self.x <= h+1:
            px = '#'
        else:
            px = '.'
        print(px, end='\n' if h == 39 else '')

        if (self.clock - 20) % 40 == 0:
            signal_strength = self.clock * self.x
            # print(f'{self.clock}: reg={self.x} ({signal_strength=})')
            self.sum_signal_strength += signal_strength
        self.clock += 1

    def add(self, val):
        self.x += val


def q1(input):
    cpu = Cpu()
    for instruction in input:
        cpu.tick()
        if instruction[:4] == 'addx':
            cpu.tick()
            cpu.add(int(instruction.split()[1]))

    return cpu.sum_signal_strength
