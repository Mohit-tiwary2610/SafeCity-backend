import numpy as np
from sklearn.cluster import DBSCAN

def cluster_points(points, eps=0.002, min_samples=5):
    coords = np.array(points)  # [[lat, lng], ...]
    return DBSCAN(eps=eps, min_samples=min_samples).fit(coords)