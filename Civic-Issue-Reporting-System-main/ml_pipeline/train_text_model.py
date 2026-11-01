"""
Train Civic Complaint Text Classifier
-------------------------------------
Trains and evaluates a text classification pipeline on municipal_training_set_cleaned.csv.
Predicts the civic complaint category (`issue_type`) from `issue_description`.

Requirements:
- Clean and preprocess text carefully.
- Handle class imbalance via class weighting.
- Split data into training, validation, and test sets without data leakage.
- Evaluate per-class precision, recall, F1-score, and a confusion matrix.
- Save trained pipeline and metadata.
- Avoid target leakage (uses ONLY issue_description as predictive input).
"""

import os
import re
import json
import csv
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score


# Standard text cleaning regex
def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    # Normalize urgent prefixes
    text = re.sub(r'^(urgent|emergency):?', '', text, flags=re.IGNORECASE)
    # Remove URL / email patterns
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove non-alphanumeric except spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_dataset(csv_path):
    descriptions = []
    labels = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get('issue_description', '').strip()
            label = row.get('issue_type', '').strip()
            if desc and label:
                descriptions.append(clean_text(desc))
                labels.append(label)
                
    return descriptions, labels


def train_and_evaluate(csv_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    X, y = load_dataset(csv_path)
    print(f"Loaded {len(X)} records from {csv_path}")
    
    classes = sorted(list(set(y)))
    print(f"Target classes ({len(classes)}): {classes}")
    
    # 70% Train, 15% Validation, 15% Test (stratified to preserve class distribution)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )
    
    print(f"Data Split: Train={len(X_train)} ({len(X_train)/len(X)*100:.1f}%), "
          f"Val={len(X_val)} ({len(X_val)/len(X)*100:.1f}%), "
          f"Test={len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")
    
    # Candidate pipelines
    models = {
        "LogisticRegression (Balanced)": Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=3500, sublinear_tf=True)),
            ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, C=2.0, random_state=42))
        ]),
        "LinearSVC (Balanced)": Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=3500, sublinear_tf=True)),
            ('clf', LinearSVC(class_weight='balanced', max_iter=2000, random_state=42))
        ]),
        "MultinomialNB": Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=3500)),
            ('clf', MultinomialNB(alpha=0.2))
        ])
    }
    
    best_model_name = None
    best_val_f1 = -1.0
    best_pipeline = None
    
    print("\n--- Model Evaluation on Validation Set ---")
    for name, pipeline in models.items():
        pipeline.fit(X_train, y_train)
        y_val_pred = pipeline.predict(X_val)
        val_acc = accuracy_score(y_val, y_val_pred)
        val_f1_macro = f1_score(y_val, y_val_pred, average='macro')
        val_f1_weighted = f1_score(y_val, y_val_pred, average='weighted')
        print(f"[{name}] Val Acc: {val_acc*100:.2f}% | Val Macro F1: {val_f1_macro*100:.2f}% | Val Weighted F1: {val_f1_weighted*100:.2f}%")
        
        if val_f1_macro > best_val_f1:
            best_val_f1 = val_f1_macro
            best_model_name = name
            best_pipeline = pipeline
            
    print(f"\nSelected Best Model: {best_model_name} (Val Macro F1 = {best_val_f1*100:.2f}%)")
    
    # Evaluate best model on independent Test Set
    print("\n" + "="*60)
    print("FINAL TEST SET EVALUATION (Unseen Test Split)")
    print("="*60)
    
    y_test_pred = best_pipeline.predict(X_test)
    test_acc = accuracy_score(y_test, y_test_pred)
    test_f1_macro = f1_score(y_test, y_test_pred, average='macro')
    test_f1_weighted = f1_score(y_test, y_test_pred, average='weighted')
    
    print(f"Test Accuracy:    {test_acc*100:.2f}%")
    print(f"Test Macro F1:    {test_f1_macro*100:.2f}%")
    print(f"Test Weighted F1: {test_f1_weighted*100:.2f}%\n")
    
    report = classification_report(y_test, y_test_pred, target_names=classes, digits=4)
    print("Classification Report:")
    print(report)
    
    cm = confusion_matrix(y_test, y_test_pred, labels=classes)
    print("Confusion Matrix:")
    header = "          " + "".join([f"{c[:7]:>8}" for c in classes])
    print(header)
    for i, row in enumerate(cm):
        row_str = "".join([f"{val:>8}" for val in row])
        print(f"{classes[i][:9]:<10}{row_str}")
        
    # Save the trained model pipeline
    model_path = os.path.join(output_dir, "text_complaint_classifier.joblib")
    joblib.dump(best_pipeline, model_path)
    print(f"\nTrained model saved to: {model_path}")
    
    # Save metadata
    meta = {
        "model_name": best_model_name,
        "classes": classes,
        "test_accuracy": round(float(test_acc), 4),
        "test_macro_f1": round(float(test_f1_macro), 4),
        "test_weighted_f1": round(float(test_f1_weighted), 4),
        "num_classes": len(classes),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_column": "issue_description",
        "target_column": "issue_type"
    }
    meta_path = os.path.join(output_dir, "text_model_metadata.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)
    print(f"Model metadata saved to: {meta_path}")

    return best_pipeline, meta


if __name__ == "__main__":
    csv_file = r"C:\Users\Asus\Downloads\municipal_training_set_cleaned.csv"
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trained_models")
    train_and_evaluate(csv_file, out_dir)

