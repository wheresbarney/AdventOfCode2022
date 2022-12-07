# https://adventofcode.com/2022/day/7

class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        if parent:
            self.parent = parent
        else:
            self.parent = self
        self.files = {} # name: size
        self.subdirs = {} # name: Dir

    def __repr__(self):
        depth = 0
        parent = self
        while parent != parent.parent:
            depth += 1
            parent = parent.parent

        repr = (depth * '  ')
        repr += f'{self.name}: {len(self.files)} files, total {sum(self.files.values())}: {self.files}'
        for sub in self.subdirs.values():
            repr += '\n' + sub.__repr__()
        return repr

    def size(self):
        size = sum(self.files.values())
        size += sum([sub.size() for sub in self.subdirs.values()])
        return size


def parse(input):
    root = Dir('/')
    current_dir = None

    for line in input:
        if line[0] == '$':
            cmd = line[2:]
            if cmd[:2] == 'cd':
                target = cmd[3:]
                if target == '/':
                    current_dir = root
                elif target == '..':
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.subdirs[target]
            else: # ls
                continue
        else: # ls output
            words = line.split(' ')
            if words[0] == 'dir':
                current_dir.subdirs[words[1]] = Dir(words[1], current_dir)
            else:
                current_dir.files[words[1]] = int(words[0])

    # print(root)
    return root

def sum_if_max(max, root, sum=0):
    for sub in root.subdirs.values():
        size = sub.size()
        if size <= max:
            sum += size
        sum = sum_if_max(max, sub, sum)
    return sum

def q1(input):
    root = parse(input)
    return sum_if_max(100000, root)

def smallest_over(min, root, smallest=None):
    size = root.size()
    if size >= min and (smallest is None or size < smallest):
        # print(f'new smallest: {root.name}, {size=}')
        smallest = size
    for sub in root.subdirs.values():
        smallest = smallest_over(min, sub, smallest)
    return smallest

def q2(input):
    root = parse(input)
    fs = 70000000
    up = 30000000
    current = root.size()
    req = current - fs + up
    if req <= 0:
        return 0
    return smallest_over(req, root)
