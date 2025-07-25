import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ✅ Auto-create output folder
os.makedirs("output", exist_ok=True)

# Load features
df = pd.read_csv("data/features.csv")

# Extract wallet separately
wallets = df["wallet"]
X = df.drop(columns=["wallet"])

# Normalize features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Risk formula (adjust weights)
score = (X_scaled[:, 1] * 0.4 + X_scaled[:, 2] * 0.3 - X_scaled[:, 3] * 0.3) * 1000

# Add score
df["score"] = score.astype(int)

# ✅ Save to guaranteed folder
df[["wallet", "score"]].to_csv("output/wallet_scores.csv", index=False)

print("✅ Scoring complete. Check output/wallet_scores.csv")
