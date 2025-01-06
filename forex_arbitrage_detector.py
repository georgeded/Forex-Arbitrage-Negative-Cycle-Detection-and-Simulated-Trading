import networkx as nx
import matplotlib.pyplot as plt
import math
import requests

API_URL = " https://example.com/api/forex"

last_fetched_data = None

def fetch_forex_rates(api_url):
    global last_fetched_data

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data == last_fetched_data:
            print("Data has not changed, using cached data.")
            return last_fetched_data["rates"], last_fetched_data["currencies"]
        else:
            last_fetched_data = data
            return data["rates"], data["currencies"]
    else:
        raise Exception(f"Failed to fetch rates. HTTP Status Code: {response.status_code}")

def build_graph_from_rates(rates):
    G = nx.DiGraph()
    for pair, rate in rates.items():
        base, quote = pair.split("/")
        G.add_edge(base, quote, weight=-math.log(rate))
    return G

def bellman_ford_all_cycles(G):
    nodes = list(G.nodes())
    all_cycles = []
    most_negative_cycles = []
    most_negative_value = float('inf')

    for source in nodes:

        dist = {node: float('inf') for node in nodes}
        pred = {node: None for node in nodes}
        dist[source] = 0

        for _ in range(len(nodes) - 1):
            for u, v, data in G.edges(data=True):
                if dist[u] + data['weight'] < dist[v]:
                    dist[v] = dist[u] + data['weight']
                    pred[v] = u

        for u, v, data in G.edges(data=True):
            if dist[u] + data['weight'] < dist[v]:
                cycle = []
                visited = set()
                x = v

                while x not in visited:
                    visited.add(x)
                    cycle.append(x)
                    x = pred[x]

                cycle.append(x)
                cycle = cycle[cycle.index(x):] 

                try:
                    cycle_weight = sum(
                        G[cycle[i]][cycle[i + 1]]['weight'] for i in range(len(cycle) - 1)
                    )
                except KeyError:
                    cycle.reverse()
                    try:
                        cycle_weight = sum(
                            G[cycle[i]][cycle[i + 1]]['weight'] for i in range(len(cycle) - 1)
                        )
                    except KeyError:
                        print(f"Invalid cycle detected, skipping: {cycle}")
                        continue

                if cycle not in all_cycles:
                    all_cycles.append((cycle, cycle_weight))

                if cycle_weight < most_negative_value:
                    most_negative_cycles = [cycle]
                    most_negative_value = cycle_weight
                elif cycle_weight == most_negative_value and cycle not in most_negative_cycles:
                    most_negative_cycles.append(cycle)

    return most_negative_cycles, math.exp(-most_negative_value) if most_negative_cycles else None, all_cycles

def detect_arbitrage_opportunities(api_url):
    try:
        rates, currencies = fetch_forex_rates(api_url)

        G = build_graph_from_rates(rates)

        most_negative_cycles, profitability, all_cycles = bellman_ford_all_cycles(G)

        result = {}
        if most_negative_cycles:
            for cycle in most_negative_cycles:
                cycle_weight = sum(G[cycle[i]][cycle[i + 1]]['weight'] for i in range(len(cycle) - 1))
                cycle_profitability = math.exp(-cycle_weight)
                percentage_profit = (cycle_profitability - 1) * 100
                result[tuple(cycle)] = {
                    "percentage_profit": percentage_profit,
                    "total_weight": cycle_weight
                }
        return result

    except Exception as e:
        print(f"Error fetching or processing rates: {e}")
        return {}