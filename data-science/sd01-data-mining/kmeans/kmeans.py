import numpy as np
import pandas as pd


def get_points():
    df = pd.read_csv("data.csv")
    X = df.iloc[:, 1:]
    return X.to_numpy()


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


def update_clusters(S, centroids):
    dists = np.linalg.norm(S[:, np.newaxis, :] - centroids[np.newaxis, :, :], axis=-1)
    return np.argmin(dists, axis=1)


def update_centroids(centroids, S, cluster, k):
    # Initialize sums and counts
    sums = np.zeros((k, S.shape[1]))
    counts = np.zeros(k)

    # Accumulate sums and counts
    np.add.at(sums, cluster, S)
    counts += np.bincount(cluster, minlength=k)

    # Avoid division by zero
    counts[counts == 0] = 1  # Prevent division by zero for empty clusters

    # Calculate new centroids
    centroids[:] = sums / counts[:, np.newaxis]

    return centroids


def kmeans(S, k):
    centroids = get_centroids(S, k, 1)
    prev_centroids = np.zeros(centroids.shape)

    cluster = np.zeros(S.shape[0])

    iteration = 0

    while not np.array_equal(centroids, prev_centroids):
        prev_centroids[:] = centroids

        cluster = update_clusters(S, centroids)
        update_centroids(centroids, S, cluster, k)

        iteration += 1

    print(f"Done after {iteration} iterations")
    print()

    for i in range(k):
        print(f"Cluster {i}: {np.sum(cluster == i)} points")


def main():
    S = get_points()
    k = 8

    kmeans(S, k)


if __name__ == "__main__":
    main()
