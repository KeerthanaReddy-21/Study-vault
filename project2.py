# studyvault_ml_dl.py
# ---------------------------------
# MACHINE LEARNING & DEEP LEARNING LOGIC FOR STUDY VAULT

import numpy as np
import random
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# -------------------------------
# ML MODEL: Study Time Prediction
# -------------------------------
def predict_study_time(prev_hours, sleep_hours):
    X = np.array([[1, 6], [2, 7], [3, 8], [4, 6], [5, 7]])
    y = np.array([2, 3, 4, 4.5, 5])

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[prev_hours, sleep_hours]])
    return float(pred[0])

# -------------------------------
# ML MODEL: Notes Classification
# -------------------------------
def classify_notes(text):
    docs = [
        "physics electricity magnetism current",
        "mathematics algebra calculus theorem",
        "computer programming python java code",
        "biology cells human body genetics",
    ]

    labels = ["Physics", "Mathematics", "Computer Science", "Biology"]

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(docs, labels)

    return model.predict([text])[0]

# -------------------------------
# DL-LIKE: Topic Recommendation (Simulated)
# -------------------------------
def recommend_topics(subject):
    topics = {
        "Physics": ["Laws of Motion", "Thermodynamics", "Optics"],
        "Mathematics": ["Linear Algebra", "Probability", "Trigonometry"],
        "Computer": ["Data Structures", "Machine Learning", "Databases"],
        "Biology": ["Genetics", "Ecology", "Anatomy"],
    }

    for key in topics:
        if key.lower() in subject.lower():
            return topics[key]

    return ["General Study Tips", "Time Management", "Revision Techniques"]

# -------------------------------
# DL-LIKE: Quiz Generator from Text
# -------------------------------
def generate_quiz_from_text(text):
    words = text.split()
    questions = []

    for i in range(min(5, len(words))):
        w = random.choice(words)
        questions.append(f"Explain the concept of '{w}'")

    return questions
