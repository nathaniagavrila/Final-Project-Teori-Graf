# 🚇 MROUTE: Singapore MRT Tourist Route Planner

> **Optimizing Singapore tourism routes using TSP and Dijkstra's Algorithm**

---

## 📋 Table of Contents

- [Background](#background)
- [Objectives](#objectives)
- [Features](#features)
- [Project Structure](#project-structure)
- [Algorithms](#algorithms)
- [MRT Line Reference](#mrt-line-reference)
- [Available Tourist Destinations](#available-tourist-destinations)
- [How to Run](#how-to-run)
- [Dependencies](#dependencies)

---

## 📌 Background

Singapore's MRT system is one of the primary transportation modes for tourists due to its wide network coverage and accessibility. However, tourists often face challenges when planning visits to multiple destinations in a single trip, determining the optimal visitation order and selecting the most efficient MRT route can be difficult and time-consuming.

Poor route planning can result in unnecessarily long travel times and excessive line transfers, reducing the overall tourist experience.

This problem can be modeled using **graph theory**, where each tourist destination is represented as a **node** and the connections between locations are represented as **weighted edges** based on travel time or number of transfers. Using the **Travelling Salesman Problem (TSP)** and **Dijkstra's Algorithm**, this application finds the most optimal and efficient travel route.

---

## 🎯 Objectives

The goal of MROUTE is to help tourists determine the best order of destinations and the most efficient MRT route in Singapore. The application leverages:

- **Dijkstra's Algorithm** — to find the shortest path (minimum travel time) between two MRT stations
- **Travelling Salesman Problem (TSP)** — to determine the optimal visitation order across multiple destinations

The system produces travel recommendations optimized for either **minimum total travel time** or **minimum number of MRT line transfers**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🕐 Fastest Route (TSP) | Finds the destination order with the minimum total travel time |
| 🔄 Least Transfer Route | Finds the destination order with the fewest MRT line changes |
| 🚫 No-Transfer Route | Checks if a full itinerary can be completed without any line transfers |
| 📊 Route Visualization | Displays the MRT network and highlights the selected route with line colors |
| 📋 Detailed Route Breakdown | Shows step-by-step path, travel time, and transfer stations for each leg |

---

## 📁 Project Structure

```
mrt-route-planner/
├── __pycache__/          # Python bytecode cache (auto-generated)
├── dataset/
│   └── MRT Stations.csv  # MRT station data (name, code, coordinates)
├── .gitignore            # Git ignored files configuration
├── archive.zip           # Project archive
├── graph.py              # Graph construction, Dijkstra, TSP functions
├── main.py               # Main script: user input, TSP, route output
├── places.py             # Dictionary of tourist destinations → MRT codes
└── visualization.py      # Route visualization using NetworkX & Matplotlib
```

---

## ⚙️ Algorithms

### Dijkstra's Algorithm

Used to find the **shortest travel time** between any two MRT station codes.

- Each MRT station code is a **node** in the graph
- Edges between adjacent stations on the same line have a weight of **2 minutes** (travel time)
- Edges between codes at the same interchange station have a weight of **5 minutes** (transfer time)
- Standard min-heap priority queue implementation

### Travelling Salesman Problem (TSP)

Used to determine the **optimal order** to visit all selected destinations.

- Evaluates **all permutations** of the destination list
- Two optimization criteria:
  - **Fastest Route**: minimizes total travel time
  - **Least Transfer Route**: minimizes total number of line transfers (uses travel time as a tiebreaker)

---

## 🗺️ MRT Line Reference

| Line | Code | Color |
|---|---|---|
| East West Line | EW | 🟢 Green  |
| North South Line | NS | 🔴 Red |
| Downtown Line | DT | 🔵 Blue |
| Circle Line | CC | 🟠 Orange  |
| North East Line | NE | 🟣 Purple  |
| Thomson-East Coast Line | TE | 🟤 Brown  |

---

## 📍 Available Tourist Destinations

The following destinations are pre-configured in `places.py`:

| Destination | MRT Code | Station |
|---|---|---|
| Lavender Hotel | EW11 | Lavender |
| Chinatown | DT19 | Chinatown |
| Gardens by the Bay | DT16 | Bayfront |
| Orchard Road | NS22 | Orchard |
| Singapore Botanic Gardens | DT9 | Botanic Gardens |
| Marina Bay Sands | DT16 | Bayfront |
| Merlion Park | NS27 | Marina Bay |
| Little India | DT12 | Little India |
| Clarke Quay | NE5 | Clarke Quay |

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install pandas matplotlib networkx
```

### 2. Run the Application

```bash
python main.py
```

### 3. Follow the Prompts

```
===== MRT TOURIST ROUTE PLANNER =====
Available places:
- Lavender Hotel
- Chinatown
- Gardens by the Bay
- ...

Input your starting point: Lavender Hotel
Input number of destinations: 4
Input destination 1: Chinatown
Input destination 2: Gardens by the Bay
Input destination 3: Singapore Botanic Gardens
Input destination 4: Orchard Road
```

### 4. Output

The application will display:

- **TSP Result** — the fastest route and total travel time
- **Least Transfer Result** — the route with fewest line changes
- **No-Transfer Route** — whether a transfer-free path exists for the full itinerary
- **Visualizations** — two route maps rendered using Matplotlib

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `pandas` | Loading and parsing MRT station CSV data |
| `networkx` | Building and drawing the MRT graph |
| `matplotlib` | Rendering route visualizations |
| `re` | Parsing MRT station codes |
| `heapq` | Priority queue for Dijkstra |
| `collections` | `defaultdict` for graph structure |
| `itertools` | `permutations` for TSP brute-force |

---

## 👥 Authors

This project was developed to fulfill the final project assignment of the Graph Theory course.
