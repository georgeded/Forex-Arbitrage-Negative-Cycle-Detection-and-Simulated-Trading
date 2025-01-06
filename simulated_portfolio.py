import time
import os
import random
from forex_arbitrage_detector import fetch_forex_rates, build_graph_from_rates, bellman_ford_all_cycles, detect_arbitrage_opportunities

API_URL = " https://example.com/api/forex"

portfolio_balance = [
    {"currency": "USD", "balance": 1},
    {"currency": "EUR", "balance": 1},
    {"currency": "GBP", "balance": 1},
    {"currency": "JPY", "balance": 1},
    {"currency": "CHF", "balance": 1},
    {"currency": "AUD", "balance": 1},
    {"currency": "CAD", "balance": 1},
    {"currency": "NZD", "balance": 1},
    {"currency": "SEK", "balance": 1},
    {"currency": "NOK", "balance": 1},
    {"currency": "ZAR", "balance": 1},
    {"currency": "INR", "balance": 1},
    {"currency": "BRL", "balance": 1},
    {"currency": "MXN", "balance": 1},
    {"currency": "SGD", "balance": 1},
    {"currency": "HKD", "balance": 1}
]

def get_balance(currency):
    for entry in portfolio_balance:
        if entry["currency"] == currency:
            return entry["balance"]
    return float('inf')

def pick_best_cycle(cycles):
    if not cycles:
        return None
    min_balance = float('inf')
    best_cycle = None
    for cycle in cycles:
        start_currency = cycle[0]
        balance = get_balance(start_currency)
        if balance < min_balance:
            min_balance = balance
            best_cycle = cycle
        elif balance == min_balance:
            best_cycle = random.choice([best_cycle, cycle])
    return best_cycle

def simulated_trading(opportunities):
    try:
        if opportunities:
            best_cycle = pick_best_cycle(opportunities.keys())
            profitability = opportunities[best_cycle]['percentage_profit']
            cycle_weight = opportunities[best_cycle]['total_weight']

            if best_cycle[0] in [entry["currency"] for entry in portfolio_balance]:
                if cycle_weight > 0 and profitability < 0:
                    print("Cycle weight is positive and profit is negative. Trade not executed.")
                else:
                    for entry in portfolio_balance:
                        if entry["currency"] == best_cycle[0]:
                            entry["balance"] *= (1 + profitability / 100) 
                            print()
                            
                    print(f"Full cycle trade execution with profit {profitability:.2f}% and cycle weight {cycle_weight:.4f}: ", end="")
                    cycle_str = "->".join(best_cycle)
                    print(cycle_str)
                    print("----------------------------------------------------------------------")
                    print("Portfolio balance after trade:")
                    for entry in portfolio_balance:
                        print(f"{entry['currency']}: {entry['balance']:.2f} {entry['currency']}")
                    print("----------------------------------------------------------------------")
        else:
            print("No arbitrage cycle detected.")
    except Exception as e:
        print(f"Error: {e}")


while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\nFetching new Forex rates...")

    opportunities = detect_arbitrage_opportunities(API_URL)
    simulated_trading(opportunities)

    if not opportunities:
        print("No negative cycle detected.")

    time.sleep(10)
