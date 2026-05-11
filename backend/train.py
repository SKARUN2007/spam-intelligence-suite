import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import requests

# Set paths relative to script location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'sms_spam.csv')
ENSEMBLE_MODEL_PATH = os.path.join(BASE_DIR, 'model', 'ensemble_model.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'tfidf_vectorizer.joblib')

def download_data():
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/sms_spam.csv"
    if not os.path.exists(DATA_PATH):
        print("Downloading dataset...")
        response = requests.get(url)
        with open(DATA_PATH, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("Dataset already exists.")

def train_advanced_model():
    # Load data
    df = pd.read_csv(DATA_PATH)
    
    # Preprocessing
    X = df['text']
    y = df['type'].map({'spam': 1, 'ham': 0})
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # TF-IDF Vectorization (Advanced)
    print("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Individual Models for Ensemble
    nb = MultinomialNB()
    svm = SVC(probability=True, kernel='linear')
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Voting Ensemble (Advanced)
    print("Training Ensemble Model (NB + SVM + Random Forest)...")
    ensemble = VotingClassifier(
        estimators=[('nb', nb), ('svm', svm), ('rf', rf)],
        voting='soft'
    )
    
    ensemble.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = ensemble.predict(X_test_vec)
    print(f"Ensemble Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save components
    print("Saving Advanced Ensemble components...")
    os.makedirs(os.path.dirname(ENSEMBLE_MODEL_PATH), exist_ok=True)
    joblib.dump(ensemble, ENSEMBLE_MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("Done.")

if __name__ == "__main__":
    download_data()
    train_advanced_model()
