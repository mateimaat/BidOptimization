import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

MAX_UNIQUE_PRICES = 20
RANDOM_STATE = 42


def load_data(bids_path):
    bids = pd.read_csv(bids_path)
    return bids


def build_price_map(bids, n_clusters=MAX_UNIQUE_PRICES):
    price_weights = (
        bids.groupby("Price")["Volume"]
        .apply(lambda v: v.abs().sum())
        .reset_index()
        .rename(columns={"Volume": "Weight"})
    )
    ## for each row calculate the entire volume of all bids
    prices = price_weights["Price"].values.reshape(-1, 1)
    weights = price_weights["Weight"].values
    ## extract values as nuympy arrays
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
## finds all the bids in the same hour and the same mapped price and sums their volumes

def run_pipeline(bids_path):
    bids = load_data(bids_path)

    price_map, centroids = build_price_map(bids)
    consolidated = apply_price_map(bids, price_map)

    return consolidated, centroids


if __name__ == "__main__":
    consolidated, centroids = run_pipeline("bids.csv")
    consolidated.to_csv("mapped_bids.csv", index=False)
    pd.DataFrame({"Centroid": sorted(centroids)}).to_csv("centroids.csv", index=False)
    print("Saved mapped_bids.csv, centroids.csv")