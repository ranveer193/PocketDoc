import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin_min, accuracy_score
from functools import lru_cache
import hashlib

# Load the training dataset
train_data = pd.read_csv("./dataset/Training.csv")

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
num_clusters = 50  # You can adjust this based on your dataset
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

# Helper function to generate a cache key
def generate_cache_key(symptom_input):
    symptom_input_str = ",".join(map(str, symptom_input))
    return hashlib.md5(symptom_input_str.encode()).hexdigest()

# Apply caching to the prediction function
@lru_cache(maxsize=1000)  # Caches the last 1000 predictions
def cached_predict(symptom_input_key):
    # Convert the key back to the original symptom_input format
    symptom_input = list(map(float, symptom_input_key.split(',')))

    input_data = pd.DataFrame([symptom_input], columns=train_data_cleaned.columns)
    scaled_input = scaler.transform(input_data)
    pca_input = pca.transform(scaled_input)  # Apply PCA transformation to the input

    kmeans_pred = kmeans.predict(pca_input)
    gmm_pred = gmm.predict(pca_input)
    agg_pred = predict_with_agglomerative(pca_input, agg_labels, pca_train_data)

    predicted_disease_kmeans = cluster_to_disease_kmeans[kmeans_pred[0]]
    predicted_disease_gmm = cluster_to_disease_gmm[gmm_pred[0]]
    predicted_disease_agg = cluster_to_disease_agg[agg_pred]

    return {
        'KMeans Prediction': predicted_disease_kmeans,
        'GMM Prediction': predicted_disease_gmm,
        'Agglomerative Prediction': predicted_disease_agg,
        'Ensemble Prediction': predicted_disease_kmeans  # Using KMeans as fallback for ensemble
    }

# Function to predict disease based on symptom input with caching
def predict_disease(symptom_input):
    assert len(symptom_input) == train_data_cleaned.shape[1], f"Input must have {train_data_cleaned.shape[1]} symptoms, but got {len(symptom_input)}."
    
    # Generate a unique key for this symptom input for caching
    symptom_input_key = ",".join(map(str, symptom_input))
    
    # Check cache first
    return cached_predict(symptom_input_key)

# # Now, let's test the accuracy using the test dataset
# test_data = pd.read_csv("./dataset/Testing.csv")

# # Preprocess the test data
# test_data_cleaned = test_data.drop([col for col in test_data.columns if 'Unnamed' in col or col == 'prognosis'], axis=1)
# test_prognosis = test_data['prognosis']

# # Standardize and apply PCA on the test data
# scaled_test_data = scaler.transform(test_data_cleaned)
# pca_test_data = pca.transform(scaled_test_data)

# # Make predictions on the test data and compare with actual results
# kmeans_predictions = []
# gmm_predictions = []
# agg_predictions = []
# ensemble_predictions = []

# for i in range(len(pca_test_data)):
#     predictions = predict_disease(test_data_cleaned.iloc[i].values)

#     kmeans_predictions.append(predictions['KMeans Prediction'])
#     gmm_predictions.append(predictions['GMM Prediction'])
#     agg_predictions.append(predictions['Agglomerative Prediction'])
#     ensemble_predictions.append(predictions['Ensemble Prediction'])

# # Calculate accuracy
# accuracy_kmeans = accuracy_score(test_prognosis, kmeans_predictions) * 100
# accuracy_gmm = accuracy_score(test_prognosis, gmm_predictions) * 100
# accuracy_agg = accuracy_score(test_prognosis, agg_predictions) * 100
# accuracy_ensemble = accuracy_score(test_prognosis, ensemble_predictions) * 100

# # Output the accuracies
# print(f"KMeans Accuracy: {accuracy_kmeans:.2f}%")
# print(f"GMM Accuracy: {accuracy_gmm:.2f}%")
# print(f"Agglomerative Accuracy: {accuracy_agg:.2f}%")
# print(f"Ensemble Accuracy: {accuracy_ensemble:.2f}%")

# # Example input
# user_input = [0, 1, 0, ...]  # Replace with actual symptom values

# # Predict the disease
# predictions = predict_disease(user_input)

# # Print the predictions from all models
# print("Predicted Disease using KMeans:", predictions['KMeans Prediction'])
# print("Predicted Disease using GMM:", predictions['GMM Prediction'])
# print("Predicted Disease using Agglomerative Clustering:", predictions['Agglomerative Prediction'])
# print("Predicted Disease using Ensemble Model:", predictions['Ensemble Prediction'])
