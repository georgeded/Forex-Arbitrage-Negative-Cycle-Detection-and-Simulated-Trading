# Leveraging Graph Theory for Forex Arbitrage: Negative Cycle Detection and Simulated Trading

This project leverages graph theory to detect arbitrage opportunities in the Forex market by identifying negative cycles in a graph representation of currency exchange rates. It also includes a simulated trading environment to execute trades based on detected arbitrage opportunities.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [API](#api)
- [Simulated Trading](#simulated-trading)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/forex-arbitrage.git
    cd forex-arbitrage
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Start the WebSocket API server:
    ```sh
    python3 server.py
    ```

2. Run the client to connect to the WebSocket server:
    ```sh
    python3 client.py
    ```

3. Run the simulated trading environment:
    ```sh
    python3 simulated_portfolio.py
    ```

## Files

- `server.py`: Flask-SocketIO server that provides real-time Forex rates updates.
- `client.py`: Client that connects to the WebSocket server and receives Forex rates updates.
- [forex_arbitrage_detector.py](http://_vscodecontentref_/1): Contains functions to fetch Forex rates, build a graph, detect negative cycles, and identify arbitrage opportunities.
- [simulated_portfolio.py](http://_vscodecontentref_/2): Simulated trading environment that executes trades based on detected arbitrage opportunities.

## API

### Forex Rates API

The server provides an endpoint to fetch the latest Forex rates.

- **Endpoint**: `/api/rates`
- **Method**: `GET`
- **Response**:
    ```json
    {
        "currencies": ["USD", "EUR", "GBP", ...],
        "rates": {
            "USD/EUR": 1.1234,
            "EUR/GBP": 0.8765,
            ...
        }
    }
    ```

## Simulated Trading

The simulated trading environment fetches Forex rates, detects arbitrage opportunities, and executes trades based on the detected opportunities.

### Functions

- [fetch_forex_rates(api_url)](http://_vscodecontentref_/3): Fetches the latest Forex rates from the API.
- [build_graph_from_rates(rates)](http://_vscodecontentref_/4): Builds a directed graph from the Forex rates.
- [bellman_ford_all_cycles(G)](http://_vscodecontentref_/5): Detects all negative cycles in the graph using the Bellman-Ford algorithm.
- [detect_arbitrage_opportunities(api_url)](http://_vscodecontentref_/6): Detects arbitrage opportunities by identifying negative cycles in the graph.
- [simulated_trading(opportunities)](http://_vscodecontentref_/7): Executes trades based on detected arbitrage opportunities.

## License

This project is licensed under the MIT License. See the LICENSE file for details.