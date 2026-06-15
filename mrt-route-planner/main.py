import pandas as pd
import re
import heapq
from collections import defaultdict
from itertools import permutations

df = pd.read_csv("dataset/MRT Stations.csv")

def extract_codes(stn_no):
    return str(stn_no).split("/")

def parse_code(code):
    match = re.match(r"([A-Z]+)(\d+)", code)
    if match:
        return match.group(1), int(match.group(2))
    return None, None

line_stations = defaultdict(list)
station_codes = defaultdict(list)
code_to_station = {}
graph = defaultdict(list)

for _, row in df.iterrows():
    station_name = row["STN_NAME"].replace(" MRT STATION", "")
    codes = extract_codes(row["STN_NO"])

    for code in codes:
        line, number = parse_code(code)
        if line:
            line_stations[line].append((number, code, station_name))
            station_codes[station_name].append(code)
            code_to_station[code] = station_name

TRAVEL_TIME = 2
TRANSFER_TIME = 5

# Edge antarstasiun dalam line sama
for line, stations in line_stations.items():
    stations = sorted(stations, key=lambda x: x[0])

    for i in range(len(stations) - 1):
        _, code_a, _ = stations[i]
        _, code_b, _ = stations[i + 1]

        graph[code_a].append((code_b, TRAVEL_TIME))
        graph[code_b].append((code_a, TRAVEL_TIME))

# Edge transit/interchange
for station, codes in station_codes.items():
    if len(codes) > 1:
        for i in range(len(codes)):
            for j in range(i + 1, len(codes)):
                code_a = codes[i]
                code_b = codes[j]

                graph[code_a].append((code_b, TRANSFER_TIME))
                graph[code_b].append((code_a, TRANSFER_TIME))


def dijkstra(start_code, end_code):
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    distances[start_code] = 0
    pq = [(0, start_code)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end_code:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    path = []
    current = end_code

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return distances[end_code], path

def count_transfers(path):
    transfers = 0
    transfer_stations = []

    for i in range(len(path) - 1):
        current_code = path[i]
        next_code = path[i + 1]

        current_station = code_to_station[current_code]
        next_station = code_to_station[next_code]

        current_line = re.match(r"([A-Z]+)", current_code).group(1)
        next_line = re.match(r"([A-Z]+)", next_code).group(1)

        # transit terjadi kalau nama stasiunnya sama, tapi line berbeda
        if current_station == next_station and current_line != next_line:
            transfers += 1
            transfer_stations.append(current_station)

    return transfers, transfer_stations


def print_route(start_code, end_code):
    total_time, path = dijkstra(start_code, end_code)
    transfers, transfer_stations = count_transfers(path)

    print(f"\nRute dari {code_to_station[start_code]} ke {code_to_station[end_code]}")
    print("Total waktu:", total_time, "menit")
    print("Jumlah transit:", transfers)

    if transfer_stations:
        print("Transit di:", ", ".join(transfer_stations))

    print("Path:")
    for code in path:
        print(f"{code} - {code_to_station[code]}")

tourist_stations = {
    "Lavender": "EW11",
    "Chinatown": "DT19",
    "Bayfront": "DT16",
    "Orchard": "NS22",
    "Botanic Gardens": "DT9"
}

def get_distance(station_a, station_b):
    code_a = tourist_stations[station_a]
    code_b = tourist_stations[station_b]

    distance, _ = dijkstra(code_a, code_b)

    return distance

def tsp_route(start, destinations):

    best_route = None
    best_cost = float("inf")

    for route in permutations(destinations):

        current_route = [start] + list(route) + [start]

        total_cost = 0

        for i in range(len(current_route)-1):

            total_cost += get_distance(
                current_route[i],
                current_route[i+1]
            )

        if total_cost < best_cost:
            best_cost = total_cost
            best_route = current_route

    return best_route, best_cost

def print_tsp_detail(route):
    total_time = 0
    total_transfers = 0

    print("\n===== ROUTE DETAILS =====")

    for i in range(len(route) - 1):
        start_station = route[i]
        end_station = route[i + 1]

        start_code = tourist_stations[start_station]
        end_code = tourist_stations[end_station]

        time, path = dijkstra(start_code, end_code)
        transfers, transfer_stations = count_transfers(path)

        total_time += time
        total_transfers += transfers

        print(f"\n{start_station} → {end_station}")
        print(f"Time: {time} minutes")
        print(f"Transfers: {transfers}")

        if transfer_stations:
            print("Transfer at:", ", ".join(transfer_stations))

        print("MRT Path:")
        for code in path:
            print(f"  {code} - {code_to_station[code]}")

    print("\n===== TOTAL SUMMARY =====")
    print("Total Travel Time:", total_time, "minutes")
    print("Total Transfers:", total_transfers)

def get_transfer_and_time(station_a, station_b):
    code_a = tourist_stations[station_a]
    code_b = tourist_stations[station_b]

    time, path = dijkstra(code_a, code_b)
    transfers, _ = count_transfers(path)

    return transfers, time

def tsp_least_transfer(start, destinations):
    best_route = None
    best_transfers = float("inf")
    best_time = float("inf")

    for route in permutations(destinations):
        current_route = [start] + list(route) + [start]

        total_transfers = 0
        total_time = 0

        for i in range(len(current_route) - 1):
            transfers, time = get_transfer_and_time(
                current_route[i],
                current_route[i + 1]
            )

            total_transfers += transfers
            total_time += time

        if total_transfers < best_transfers:
            best_transfers = total_transfers
            best_time = total_time
            best_route = current_route

        elif total_transfers == best_transfers and total_time < best_time:
            best_time = total_time
            best_route = current_route

    return best_route, best_transfers, best_time

print("===== MRT TOURIST ROUTE PLANNER =====")
print("Available sample stations:")
print("Lavender, Chinatown, Bayfront, Orchard, Botanic Gardens")

start = input("\nInput start station: ")

n = int(input("Input number of destinations: "))

destinations = []

for i in range(n):
    destination = input(f"Input destination {i+1}: ")
    destinations.append(destination)

best_route, best_cost = tsp_route(start, destinations)

print("\n===== TSP RESULT =====")
print("Best Route:")

for station in best_route:
    print(station)

print("\nTotal Travel Time:", best_cost, "minutes")

print_tsp_detail(best_route)

least_route, least_transfers, least_time = tsp_least_transfer(start, destinations)

print("\n===== LEAST TRANSFER RESULT =====")
print("Best Route:")

for station in least_route:
    print(station)

print("\nTotal Transfers:", least_transfers)
print("Total Travel Time:", least_time, "minutes")

print_tsp_detail(least_route)

def get_lines(code):
    match = re.match(r"([A-Z]+)", code)
    return match.group(1) if match else None


def no_transfer_route(station_a, station_b):
    codes_a = station_codes[code_to_station[tourist_stations[station_a]]]
    codes_b = station_codes[code_to_station[tourist_stations[station_b]]]

    for code_a in codes_a:
        line_a = get_lines(code_a)

        for code_b in codes_b:
            line_b = get_lines(code_b)

            if line_a == line_b:
                time, path = dijkstra(code_a, code_b)
                transfers, _ = count_transfers(path)

                if transfers == 0:
                    return time, path

    return None, None

def check_full_no_transfer_route(route):
    full_path = []
    total_time = 0

    for i in range(len(route) - 1):
        station_a = route[i]
        station_b = route[i + 1]

        time, path = no_transfer_route(station_a, station_b)

        if path is None:
            return False, station_a, station_b, None, None

        total_time += time

        if i == 0:
            full_path.extend(path)
        else:
            full_path.extend(path[1:])

    return True, None, None, total_time, full_path

available, failed_from, failed_to, no_transfer_time, no_transfer_path = check_full_no_transfer_route(best_route)

print("\n===== NO TRANSFER ROUTE RESULT =====")

if available:
    print("No-transfer route available for the full itinerary")
    print("Total Travel Time:", no_transfer_time, "minutes")
    print("MRT Path:")

    for code in no_transfer_path:
        print(f"  {code} - {code_to_station[code]}")

else:
    print("No-transfer route not available for the full itinerary")
    print(f"Reason: {failed_from} → {failed_to} requires MRT line transfer")