import numpy as np

def compute_predictive_growth(data):
    trend_factor = np.random.uniform(0.9, 1.1)
    return round(data["SQGLP_Score"] * trend_factor, 2)