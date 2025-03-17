import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from matplotlib import pyplot as plt


def sse(X, kwargs: dict):
    kmeans = KMeans(**kwargs).fit(X)
    return kmeans.inertia_


def ex1(X):
    print(f"SSE = {sse(X, {"init": "random", "n_clusters": 8})}")


def ex2(X):
    print(f"SSE = {sse(X, {"init": "k-means++", "n_clusters": 8})}")
    print(f"SSE = {sse(X, {"init": "random", "n_clusters": 8, "max_iter": 28_000})}")
    print(f"SSE = {sse(X, {"init": "k-means++", "n_clusters": 8, "n_init": 1_000})}")
    print(f"SSE = {sse(X, {"init": "k-means++", "n_clusters": 8, "max_iter": 28_000, "n_init": 2_000})}")


def ex3(df):
    X = df.iloc[:, 1:]
    kmeans = KMeans(init="k-means++", n_clusters=8, max_iter=28_000, n_init=2_000).fit(X)
    labels = kmeans.labels_
    df["cluster"] = labels

    pd.set_option('display.max_colwidth', None)
    print(df.groupby("cluster")["StockName"].apply(list))
    print(f"SSE = {kmeans.inertia_}")


def d(X, C):
    dists = np.linalg.norm(X[:, np.newaxis, :] - C[np.newaxis, :, :], axis=-1)
    return np.min(dists, axis=1)


def sample_element(X, probs):
    x = np.random.rand()
    probs = np.cumsum(probs)

    closest_interval = probs[probs >= x][0]

    idx = np.where(probs == closest_interval)[0][0]
    return X[idx]


def get_centroids(S, k, method=0):
    n = S.shape[0]
    if method == 0:
        return S[np.random.choice(n, size=k, replace=False)]

    C = np.array([sample_element(S, np.ones(n + 1) / n)])

    while C.shape[0] < k:
        D = np.square(d(S, C))
        D /= np.sum(D)

        x = sample_element(S, D)
        C = np.append(C, [x], axis=0)

    return C


def ex4(df):
    X = df.iloc[:, 1:]
    C = get_centroids(X.to_numpy(), 8, 1)
    kmeans = KMeans(init=C, n_clusters=8, max_iter=28_000).fit(X)
    labels = kmeans.labels_
    df["cluster"] = labels

    pd.set_option('display.max_colwidth', None)
    print(df.groupby("cluster")["StockName"].apply(list))
    print(f"SSE = {kmeans.inertia_}")


def main():
    df = pd.read_csv("data.csv")
    X = df.iloc[:, 1:]
    ex1(X)
    ex2(X)
    ex3(df)
    ex4(df)


if __name__ == "__main__":
    main()
