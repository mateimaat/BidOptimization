import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

MAX_UNIQUE_PRICES = 20
RANDOM_STATE = 42


def load_data(bids_path, forecast_path):
    bids     = pd.read_csv(bids_path)
    forecast = pd.read_csv(forecast_path)
    return bids, forecast


def build_price_map(bids, forecast, n_clusters=MAX_UNIQUE_PRICES):
    df = bids.merge(forecast, on="Hour")

    # weight = |volume| / (1 + |price - spot_forecast|)
    df["Weight"] = df["Volume"].abs() / (1 + (df["Price"] - df["SpotForecast"]).abs())

    price_weights = df.groupby("Price")["Weight"].sum().reset_index()

    prices  = price_weights["Price"].values.reshape(-1, 1)
    weights = price_weights["Weight"].values

    km = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=20)
    km.fit(prices, sample_weight=weights)

    centroids = np.round(km.cluster_centers_.flatten(), 1)

    price_map = {}
    for i, row in price_weights.iterrows():
        price_map[row["Price"]] = centroids[km.labels_[i]]

    return price_map, centroids


def apply_price_map(bids, price_map):
    mapped = bids.copy()
    mapped["MappedPrice"] = mapped["Price"].map(price_map)

    consolidated = (
        mapped.groupby(["Hour", "MappedPrice"], as_index=False)["Volume"].sum().rename(columns={"MappedPrice": "Price"})
    )
    return consolidated
# find all bids in the same hour with the same mapped price and sum their volumes

def run_pipeline(bids_path, forecast_path):
    bids, forecast = load_data(bids_path, forecast_path)
    price_map, centroids = build_price_map(bids, forecast)
    consolidated = apply_price_map(bids, price_map)
    return consolidated, centroids


if __name__ == "__main__":
    consolidated, centroids = run_pipeline("bids.csv", "spot_forecast.csv")
    consolidated.to_csv("mapped_bids_modified.csv", index=False)
    pd.DataFrame({"Centroid": sorted(centroids)}).to_csv("centroids_modified.csv", index=False)
    print("Saved mapped_bids_modified.csv, centroids_modified.csv")