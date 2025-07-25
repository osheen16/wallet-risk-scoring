import requests
import pandas as pd
import time

API_KEY = "cqt_rQ98v8jGFqvbKVYD34D7myKmkXfY"  
CHAIN_ID = 1  # Ethereum Mainnet

# Load wallets
wallets_df = pd.read_csv("data/wallet_ids.csv")
features = []

def get_transactions(wallet):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet}/transactions_v2/?key={API_KEY}&page-size=1000"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching {wallet}: {e}")
        return None

# Keywords to identify Compound actions
compound_keywords = ['compound', 'ceth', 'cdai', 'cusdc', 'supply', 'borrow', 'repay']

for wallet in wallets_df["wallet_id"]:
    wallet = wallet.strip()
    print(f"⏳ Processing {wallet}...")
    data = get_transactions(wallet)
    time.sleep(0.5)

    if not data or data.get("data") is None:
        print(f"No data for wallet {wallet}")
        continue

    txs = data["data"]["items"]

    total_supply = 0
    total_borrow = 0
    num_borrows = 0

    for tx in txs:
        log_text = tx.get("log_events", [])
        tx_text = tx.get("decoded", {}).get("name", "").lower()

        if any(word in tx_text for word in compound_keywords):
            value = float(tx.get("value", 0)) / 1e18  # ETH denomination
            if 'supply' in tx_text:
                total_supply += value
            elif 'borrow' in tx_text:
                total_borrow += value
                num_borrows += 1
            elif 'repay' in tx_text:
                total_borrow -= value  # treated as payback

    net_collateral = total_supply - total_borrow

    features.append({
        "wallet": wallet,
        "total_supplied": round(total_supply, 4),
        "total_borrowed": round(total_borrow, 4),
        "num_borrows": num_borrows,
        "net_collateral": round(net_collateral, 4)
    })

# Save to CSV
df = pd.DataFrame(features)
df.to_csv("data/features.csv", index=False)
print("✅ Done! features.csv created with", len(features), "wallets.")
