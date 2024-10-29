# first line: 37
@memory.cache  # Cache results of clustering to avoid recomputation
def run_clustering():
    with ThreadPoolExecutor(max_workers=2) as executor:
        kmeans_future = executor.submit(kmeans.fit_predict, pca_train_data)
        gmm_future = executor.submit(gmm.fit_predict, pca_train_data)
        return kmeans_future.result(), gmm_future.result()
