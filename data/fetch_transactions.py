import requests
import pandas as pd

API_KEY = "YOUR_COVALENT_KEY"
CHAIN_ID = 1  # Ethereum Mainnet

def fetch_compound_transactions(wallet):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet}/transactions_v2/"
    params = {"key": API_KEY}
    response = requests.get(url, params=params)
    return response.json()

wallets = pd.read_csv("data/wallet_ids.csv")["wallet_id"]

tx_data = []
for wallet in wallets:
    data = fetch_compound_transactions(wallet)
    # extract relevant data like method name, value, token, gas, timestamp, etc.
    tx_data.append({"wallet": wallet, "raw": data})  # Replace with parsed tx info

pd.DataFrame(tx_data).to_pickle("data/raw_transactions.pkl")
