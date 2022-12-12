# https://adventofcode.com/2022/day/12

from math import inf
from queue import PriorityQueue
from typing import Callable

class Graph:
    def __init__(self, num_of_vertices: int):
        self.v = num_of_vertices
        self.edges = [[False for i in range(self.v)] for j in range(self.v)]
        self.visited = []

    def add_edge(self, u: int, v: int):
        self.edges[u][v] = True

def is_legal_step_q1(source: str, dest: str) -> bool:
    if source == "S":
        return dest in ["a", "b"]
    if dest == "E":
        return source in ["y", "z"]
    return ord(dest) <= ord(source) + 1

def is_legal_step_q2(source: str, dest: str) -> bool:
    if source == "S" or dest == "S":
        return False
    if source == "E":
        return dest in ["y", "z"]
    return ord(dest) >= ord(source) - 1

def point_to_vertex_index(input: [str], r: int, c: int) -> int:
    return r * len(input[0]) + c

def q1(input: [str]) -> str:
    for r, row in enumerate(input):
        for c, char in enumerate(row):
            # record origin and destination
            if char == "S":
                origin = point_to_vertex_index(input, r, c)
            elif char == "E":
                dest = point_to_vertex_index(input, r, c)

    distances = solve(input, origin, is_legal_step_q1)

    return distances[dest]

def q2(input: [str]) -> str:
    destinations = []
    for r, row in enumerate(input):
        for c, char in enumerate(row):
            # record origin and destinations
            if char == "E":
                origin = point_to_vertex_index(input, r, c)
            elif char == "a":
                destinations.append(point_to_vertex_index(input, r, c))

    distances = solve(input, origin, is_legal_step_q2)

    return min([distances[dest] for dest in destinations])

def solve(input: [str], origin: int, is_legal_step: Callable[[int, int], int]) -> {int: int}:
    graph = Graph(len(input) * len(input[0]))
    up_down_left_right = {(-1, 0), (1, 0), (0, -1), (0, 1)}

    for r, row in enumerate(input):
        for c, char in enumerate(row):
            for direction in up_down_left_right:
                neighbour = (r + direction[0], c + direction[1])
                if neighbour[0] in range(len(input)) and neighbour[1] in range(len(row)):
                    other = input[neighbour[0]][neighbour[1]]
                    v1 = point_to_vertex_index(input, r, c)
                    v2 = point_to_vertex_index(input, *neighbour)
                    if is_legal_step(char, other):
                        # print(f"adding edge from {v1}[{(r, c)}:{char}] to {v2}:[{neighbour}:{other}]")
                        graph.add_edge(v1, v2)

    distances = {v:inf for v in range(graph.v)}
    distances[origin] = 0

    pq = PriorityQueue()
    pq.put((0, origin))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbour in range(graph.v):
            viable = graph.edges[current_vertex][neighbour]
            if viable:
                if neighbour not in graph.visited:
                    old_cost = distances[neighbour]
                    new_cost = distances[current_vertex] + 1
                    if new_cost < old_cost:
                        # print(f"found new path from {current_vertex} to {neighbour}, distance {new_cost}")
                        pq.put((new_cost, neighbour))
                        distances[neighbour] = new_cost

    # row_len = len(input[0])
    # for r in range(len(input)):
    #     row_start = r * row_len
    #     print(' '.join([str(distances[v]) for v in range(row_start, row_start + row_len)]))
    return distances
