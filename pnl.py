import pandas as pd

bids = pd.read_csv("mapped_bids_modified.csv")
forecast = pd.read_csv("spot_forecast.csv")

df = bids.merge(forecast, on="Hour")

buy_filled = (df["Volume"] > 0) & (df["Price"] >= df["SpotForecast"])
sell_filled = (df["Volume"] < 0) & (df["Price"] <= df["SpotForecast"])
df["Filled"] = buy_filled | sell_filled
# check if order is filled 

df["PnL"] = 0.0
df.loc[buy_filled,  "PnL"] = df["Volume"] * (df["SpotForecast"] - df["Price"])
df.loc[sell_filled, "PnL"] = - df["Volume"] * (df["Price"] - df["SpotForecast"])
# PnL 

print(df[["Hour", "Price", "Volume", "SpotForecast", "Filled", "PnL"]])
print(f"\nTotal PnL : {df['PnL'].sum():.2f} EUR")
print(f"Filled bids: {df['Filled'].sum()} / {len(df)}")
