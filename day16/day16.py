# https://adventofcode.com/2022/day/16

from collections import defaultdict
from functools import cache

def all_routes(valves, route, visited, opened):
    # assert len(route) < 15, f"excessive length {route} ({current=} {visited=} {opened=}"
    if len(route) > 30:
        # no point exploring further, won't increase pressure
        return []

    current = route[-1]
    valve = valves[current]
    ret = []

    for path in valve[1]:
        if len(route) > 1 and path == route[-2] and (valves[path] == 0 or path in opened):
            continue # no point just bouncing back
        if len(route) > 2 and route[-2] == "open" and path == route[-3] and (valves[path] == 0 or path in opened):
            continue # no point just bouncing back
        if visited[path] < len(valves[path][1]):
            local_visited = defaultdict(int, visited)
            local_visited[current] = local_visited[current] + 1
            # print(f"{route}:{current} recursing into {path} ({local_visited=} {opened=}")
            ret.extend([[current] + cr for cr in all_routes(valves, route + [path], local_visited, opened)])
            if valve[0] and current not in opened:
                local_visited = defaultdict(int, visited)
                local_visited[current] = local_visited[current] + 1
                # print(f"{route}:{current} opening and recursing into {path} ({local_visited=} {opened=}")
                ret.extend([[current, "open"] + cr for cr in all_routes(valves, route + ["open", path], local_visited, opened | {current})])

    if not ret:
        # reached end of the road
        terminal = [current]
        if valve[0] and current not in opened:
            terminal.append("open")
        ret.append(terminal)

    return ret


def q1(input: [str]) -> str:
    return solve(input, 30, False)

def q2(input: [str]) -> str:
    return solve(input, 26, True)

def solve(input, time, elephant):
    valves = [l.replace("=", " ").replace(";", "").replace(",", "").split() for l in input]
    valves = {v[1]: (int(v[5]), v[10:]) for v in valves}

    # with a lot of help from https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2022/d16_proboscidea_volcanium/valve_pressure.py
    @cache
    def calc_max_relief(current_pos, mins_remaining, elephant, opened):
        if mins_remaining <= 0:
            if elephant:
                return calc_max_relief("AA", 26, False, opened)
            return 0

        max_relief = 0
        valve = valves[current_pos]
        for neighbour in valve[1]:
            max_relief = max(max_relief, calc_max_relief(neighbour, mins_remaining - 1, elephant, opened))

        if valve[0] and current_pos not in opened and mins_remaining > 0:
            mins_remaining -= 1
            released = mins_remaining * valve[0]
            for neighbour in valve[1]:
                max_relief = max(max_relief, released + calc_max_relief(neighbour, mins_remaining - 1, elephant, frozenset(opened | {current_pos})))

        return max_relief

    return calc_max_relief("AA", time, elephant, frozenset())

    # routes = all_routes(valves, ["AA"], defaultdict(int), set())
    # print(f"identified {len(routes)} routes")

    # max_pressure_released = 0
    # best_route = None
    # for route in routes:
    #     ticks = 0
    #     pressure_released = 0
    #     for step in route:
    #         if step == "open":
    #             pressure_released += (30 - ticks) * valve[0]
    #         else:
    #             valve = valves[step]
    #         ticks += 1

    #     # print(f"{pressure_released}: {','.join(route)}")
    #     if pressure_released > max_pressure_released:
    #         max_pressure_released = pressure_released
    #         best_route = route

    # print(','.join(best_route))
    # return max_pressure_released
