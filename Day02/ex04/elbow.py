def calculate_mean(vector: list):
    """Calculate Mean"""
    return sum(x for x in vector) / len(vector)


def calculate_variance(vector: list):
    """Calculate Variance"""
    mean = calculate_mean(vector)
    return sum(pow((x - mean), 2) for x in vector) / len(vector)


def calculate_standard_deviation(vector: list):
    """Calculate Standard Deviation"""
    return calculate_variance(vector) ** 0.5


# A list holds the SSE values for each k
   ...: sse = []
   ...: for k in range(1, 11):
   ...:     kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
   ...:     kmeans.fit(scaled_features)
   ...:     sse.append(kmeans.inertia_)