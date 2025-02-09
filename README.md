# PocketDoctor

## Overview
PocketDoctor is an AI-powered healthcare assistant that predicts diseases based on user-entered symptoms and recommends suitable medicines. It utilizes an **unsupervised machine learning model** with clustering techniques to identify diseases even when there is no exact match in the dataset.

## Features
- **AI-based Disease Prediction**: Uses clustering models such as K-means, Gaussian Mixture Model (GMM), and Agglomerative Clustering.
- **Medicine Recommendation**: Maps predicted diseases to appropriate medicines.
- **Lightweight & Fast**: Optimized for minimal resource usage, making it compatible with IoT devices.
- **User Privacy**: No sensitive personal data is stored.
- **Web-Based Interface**: Simple and interactive frontend using **HTML, CSS, and JavaScript**.

## Technology Stack
- **Machine Learning Model**: Python (Scikit-learn, Pandas, NumPy)
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Node.js, Express.js
- **Database**: Pre-trained dataset for disease prediction

## Workflow
1. **User Input**: Symptoms are entered via the frontend.
2. **Data Processing**: Symptoms are preprocessed and transformed.
3. **Model Execution**:
   - The system runs the **Ensemble Model** combining K-means, GMM, and Agglomerative Clustering.
   - The most probable disease is predicted using majority voting.
4. **Medicine Recommendation**: The predicted disease is mapped to a medicine dataset.
5. **Result Display**: The user receives a disease diagnosis along with recommended medicine.

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- **Python** (for the ML model)
- **Node.js & npm** (for the backend)

### Steps
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/ranveer193/PocketDoc.git
   cd PocketDoc
   ```
2. **Install Backend Dependencies**:
   ```sh
   npm install
   ```
3. **Install Python Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Backend Server**:
   ```sh
   node server.js
   ```
5. **Run the ML Model (Standalone Testing)**:
   ```sh
   python model.py
   ```
6. **Open the Frontend**:
   - Navigate to `localhost:3000` in your browser.

## Dataset Information
- The dataset contains **132 symptoms** mapped to **42 diseases**.
- Sourced from **GeeksforGeeks Disease Prediction Dataset** ([link](https://www.geeksforgeeks.org/disease-prediction-using-machine-learning/)).

## Model Performance
| Model             | Accuracy | Precision | Recall | F1 Score |
|------------------|----------|-----------|--------|----------|
| K-Means         | 0.97     | 0.96      | 0.97   | 0.97     |
| GMM             | 0.97     | 0.96      | 0.97   | 0.97     |
| Agglomerative   | 1.00     | 1.00      | 1.00   | 1.00     |
| **Ensemble**    | **1.00** | **1.00**  | **1.00** | **1.00** |

## Future Enhancements
- **Expand Symptom Database**: Support for more diseases and symptoms.
- **Natural Language Processing (NLP)**: To understand user symptoms in layman’s terms.
- **IoT Device Integration**: Enabling input from smartwatches and health monitoring devices.
- **Personalized Medicine Suggestions**: Based on user medical history.
- **Real-Time Medical Database Integration**: Fetch latest treatment suggestions.

## Contributors
- **Ranbir Singh** (Group Leader)
- **Krishna Verma**
- **Prashant Solankey**
- **Chirag Aggarwal**
- **Meher Narayan Shetty**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Inspired by various research papers and datasets on disease prediction.
- Special thanks to **GeeksforGeeks** for their dataset.

---
Feel free to contribute and enhance **PocketDoctor**! 🚀
