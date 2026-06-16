import re
import heapq
from collections import defaultdict
from itertools import permutations
from places import PLACES


TRAVEL_TIME = 2
TRANSFER_TIME = 5


# =========================
# BUILD GRAPH
# =========================
def build_graph(df):
    line_stations = defaultdict(list)
    station_codes = defaultdict(list)
    code_to_station = {}
    graph = defaultdict(list)

    for _, row in df.iterrows():
        station_name = row["STN_NAME"].replace(" MRT STATION", "")
        codes = str(row["STN_NO"]).split("/")

        for code in codes:
            match = re.match(r"([A-Z]+)(\d+)", code)
            if match:
                line = match.group(1)
                number = int(match.group(2))

                line_stations[line].append((number, code, station_name))
                station_codes[station_name].append(code)
                code_to_station[code] = station_name

    # connect same line
    for line, stations in line_stations.items():
        stations.sort()

        for i in range(len(stations) - 1):
            _, a, _ = stations[i]
            _, b, _ = stations[i + 1]

            graph[a].append((b, TRAVEL_TIME))
            graph[b].append((a, TRAVEL_TIME))

    # transfer edges
    for station, codes in station_codes.items():
        if len(codes) > 1:
            for i in range(len(codes)):
                for j in range(i + 1, len(codes)):
                    a, b = codes[i], codes[j]
                    graph[a].append((b, TRANSFER_TIME))
                    graph[b].append((a, TRANSFER_TIME))

    return graph, station_codes, code_to_station


# =========================
# DIJKSTRA
# =========================
def dijkstra(graph, start, end):
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        cur_d, node = heapq.heappop(pq)

        if node == end:
            break

        if cur_d > dist[node]:
            continue

        for nxt, w in graph[node]:
            nd = cur_d + w

            if nd < dist[nxt]:
                dist[nxt] = nd
                prev[nxt] = node
                heapq.heappush(pq, (nd, nxt))

    path = []
    cur = end

    while cur:
        path.append(cur)
        cur = prev[cur]

    return dist[end], path[::-1]


# =========================
# TRANSFER COUNT
# =========================
def count_transfers(path, code_to_station):
    transfers = 0
    transfer_stations = []

    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]

        station_a = code_to_station[a]
        station_b = code_to_station[b]

        line_a = re.match(r"([A-Z]+)", a).group(1)
        line_b = re.match(r"([A-Z]+)", b).group(1)

        if station_a == station_b and line_a != line_b:
            transfers += 1
            transfer_stations.append(station_a)

    return transfers, transfer_stations


# =========================
# DISTANCE HELPER
# =========================
def get_distance(graph, code_to_station, a, b):
    ca = PLACES[a]
    cb = PLACES[b]
    time, _ = dijkstra(graph, ca, cb)
    return time


# =========================
# TSP TIME OPTIMIZED
# =========================
def tsp_route(graph, start, destinations, code_to_station):
    best_route = None
    best_cost = float("inf")

    for perm in permutations(destinations):
        route = [start] + list(perm) + [start]

        cost = 0
        for i in range(len(route) - 1):
            cost += get_distance(graph, code_to_station, route[i], route[i + 1])

        if cost < best_cost:
            best_cost = cost
            best_route = route

    return best_route, best_cost


# =========================
# TSP LEAST TRANSFER
# =========================
def tsp_least_transfer(graph, start, destinations, code_to_station):
    best_route = None
    best_transfer = float("inf")
    best_time = float("inf")

    for perm in permutations(destinations):
        route = [start] + list(perm) + [start]

        total_t = 0
        total_time = 0

        for i in range(len(route) - 1):
            a = PLACES[route[i]]
            b = PLACES[route[i + 1]]

            t, path = dijkstra(graph, a, b)
            tr, _ = count_transfers(path, code_to_station)

            total_transfer += tr
            total_time += t

        if total_transfer < best_transfer or (
            total_transfer == best_transfer and total_time < best_time
        ):
            best_transfer = total_transfer
            best_time = total_time
            best_route = route

    return best_route, best_transfer, best_time