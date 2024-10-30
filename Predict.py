import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin_min, accuracy_score
from functools import lru_cache
from collections import Counter
import hashlib

# Load the training dataset
train_data = pd.read_csv("./dataset/Dataset.csv")

# Preprocess the training data
train_data_cleaned = train_data.drop([col for col in train_data.columns if 'Unnamed' in col or col == 'prognosis'], axis=1)
train_prognosis = train_data['prognosis']

# Standardize the training data features
scaler = StandardScaler()
scaled_train_data = scaler.fit_transform(train_data_cleaned)

# Apply PCA for dimensionality reduction
pca = PCA(n_components=0.95)  # Retain 95% of variance
pca_train_data = pca.fit_transform(scaled_train_data)

# Initialize clustering models
num_clusters = 42  # You can adjust this based on your dataset
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans_labels = kmeans.fit_predict(pca_train_data)

gmm = GaussianMixture(n_components=num_clusters, random_state=42)
gmm_labels = gmm.fit_predict(pca_train_data)

agg_clustering = AgglomerativeClustering(n_clusters=num_clusters)
agg_labels = agg_clustering.fit_predict(pca_train_data)

# Mapping clusters to diseases based on the training data
clustered_train_df = pd.DataFrame({
    'KMeans': kmeans_labels,
    'GMM': gmm_labels,
    'Agglomerative': agg_labels,
    'Prognosis': train_prognosis
})

cluster_to_disease_kmeans = clustered_train_df.groupby('KMeans')['Prognosis'].agg(lambda x: x.value_counts().index[0])
cluster_to_disease_gmm = clustered_train_df.groupby('GMM')['Prognosis'].agg(lambda x: x.value_counts().index[0])
cluster_to_disease_agg = clustered_train_df.groupby('Agglomerative')['Prognosis'].agg(lambda x: x.value_counts().index[0])

# Function for agglomerative clustering prediction
def predict_with_agglomerative(input_sample, agg_model, training_data):
    nearest_cluster, _ = pairwise_distances_argmin_min(input_sample, training_data)
    return agg_model[nearest_cluster[0]]

def predict_disease(symptom_input):
    # Ensure the input matches the feature count of the training data
    assert len(symptom_input) == train_data_cleaned.shape[1], (
        f"Input must have {train_data_cleaned.shape[1]} symptoms, but got {len(symptom_input)}."
    )

    # Convert user input into a DataFrame for preprocessing
    input_data = pd.DataFrame([symptom_input], columns=train_data_cleaned.columns)

    # Standardize and apply PCA transformation
    scaled_input = scaler.transform(input_data)
    pca_input = pca.transform(scaled_input)

    # Predict clusters with each model
    kmeans_pred = kmeans.predict(pca_input)[0]
    gmm_pred = gmm.predict(pca_input)[0]
    
    # Find nearest cluster for Agglomerative Clustering
    nearest_cluster, _ = pairwise_distances_argmin_min(pca_input, pca_train_data)
    agg_pred = agg_labels[nearest_cluster[0]]

    # Map predicted clusters to diseases
    predicted_disease_kmeans = cluster_to_disease_kmeans.get(kmeans_pred, "Unknown")
    predicted_disease_gmm = cluster_to_disease_gmm.get(gmm_pred, "Unknown")
    predicted_disease_agg = cluster_to_disease_agg.get(agg_pred, "Unknown")

    # Ensemble prediction: Majority vote
    predictions = [predicted_disease_kmeans, predicted_disease_gmm, predicted_disease_agg]
    ensemble_prediction = Counter(predictions).most_common(1)[0][0]  # Most common disease

    return {
        'KMeans Prediction': predicted_disease_kmeans,
        'GMM Prediction': predicted_disease_gmm,
        'Agglomerative Prediction': predicted_disease_agg,
        'Ensemble Prediction': ensemble_prediction
    }
