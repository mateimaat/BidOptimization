# BidOptimization

## Overview

This project addresses a key constraint in electricity market auctions (eg. EPEX), where only a limited number of unique bid prices can be submitted.

Given a number of bids (1155 in this specific case), the goal is to reduce price diversity while preserving economic intent.

### Data

- `bids.csv` -> hourly bids (price, volume)
- `spot_forecast.csv` -> forecasted market prices

## Approach

Clustering using:

1. Volume-based Kmeans
- clusters using volume as weight
- larger poitions have more influence

2. Forecast-aware KMeans
- clusters using a custom weight
- `weight = volume / (1+ (price - spotforecast))`
- prioritizes bids closer to expected market price

## Output and evaluation

Prices are mapped to a desired number of centroids.
Evaluated using PnL based on forecast, and SSE to measure distortion.

## Visualization

Interactive dashboard to explore bids

```bash
# Run the interactive dashboard
python dashboard.py

# Run the KMeans clustering
python kmeans_volume.py
