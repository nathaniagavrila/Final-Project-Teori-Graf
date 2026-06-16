import networkx as nx
import matplotlib.pyplot as plt
from graph import dijkstra
from places import PLACES

def build_nx(graph):
    G = nx.Graph()

    for u, neighbors in graph.items():
        for v, w in neighbors:
            G.add_edge(u, v, weight=w)

    return G

def build_positions(df):
    pos = {}

    for _, row in df.iterrows():
        codes = str(row["STN_NO"]).split("/")
        lat = row["Latitude"]
        lon = row["Longitude"]

        for code in codes:
            pos[code] = (lon, lat)  # note: x=lon, y=lat

    return pos

def get_full_path(graph, route):
    full = []

    for i in range(len(route) - 1):
        a = PLACES[route[i]]
        b = PLACES[route[i + 1]]

        _, path = dijkstra(graph, a, b)

        if i == 0:
            full.extend(path)
        else:
            full.extend(path[1:])

    return full

def draw(G, pos):
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, node_size=10, edge_color="lightgray", alpha=0.5)

def show_route(G, pos, path, color):
    edges = list(zip(path, path[1:]))

    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color=color, node_size=30)
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=2)

def visualize(graph, df, route, title):
    import matplotlib.pyplot as plt
    import networkx as nx
    import re

    def get_line(code):
        match = re.match(r"([A-Z]+)", code)
        return match.group(1) if match else "UNKNOWN"

    LINE_COLORS = {
    "EW": "#009645",  # green
    "NS": "#D42E12",  # red
    "NE": "#9900CC",  # purple
    "CC": "#FA9E0D",  # orange
    "DT": "#005EC4",  # blue
    "TE": "#9D5B25",  # brown
    "CG": "#0099CC",  # changi branch
    "BP": "#999999",  # lrt bp
    "PE": "#999999",
    "PW": "#999999",
    "SE": "#999999",
    "SW": "#999999",
}

    G = nx.Graph()

    for node, edges in graph.items():
        for neighbor, w in edges:
            G.add_edge(node, neighbor)

    pos = build_positions(df)

    G = G.subgraph([n for n in G.nodes() if n in pos])

    plt.figure(figsize=(14, 10))

    nx.draw(
        G,
        pos,
        node_size=5,
        edge_color="lightgray",
        alpha=0.3
    )

    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]

        line = get_line(a)
        color = LINE_COLORS.get(line, "black")

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(a, b)],
            edge_color=color,
            width=3
        )

    nx.draw_networkx_labels(
        G,
        pos,
        labels={n: n for n in route},
        font_size=8
    )

    plt.title(title)
    plt.show()