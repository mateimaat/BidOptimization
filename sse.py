import pandas as pd
import numpy as np

bids = pd.read_csv("bids.csv")
centroids = pd.read_csv("centroids.csv").iloc[:, 0].astype(float).values

def nearest_centroid(price):
    distances = np.abs(centroids - price)
    closest = np.argmin(distances)
    return centroids[closest]

bids["Distance"] = bids["Price"].apply(nearest_centroid)
bids["SE"] = (bids["Price"] - bids["Distance"]) ** 2

sse = bids.groupby("Distance")["SE"].sum()
print(sse)
print(f"{sse.sum():.2f}")