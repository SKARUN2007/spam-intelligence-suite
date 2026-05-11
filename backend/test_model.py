import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'spam_model.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'vectorizer.joblib')

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

tests = [
    "URGENT! You have won a $1,000 gift card! Click here to claim your prize now! Limited time offer.",
    "Hi John, just checking if we are still on for the meeting at 3 PM today. Best, Sarah.",
    "Hey mom, I'll be home late today. Don't wait for dinner.",
    "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's"
]

for t in tests:
    vec = vectorizer.transform([t])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    label = "spam" if pred == 1 else "ham"
    print(f"Text: {t[:50]}...")
    print(f"Prediction: {label} ({prob[pred]*100:.2f}%)")
    print("-" * 20)
