import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, learning_curve, validation_curve
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.utils import shuffle
import joblib

# Load dataset
crop = pd.read_csv("Crop_recommendation.csv")

# Encode categorical data
label_encoder = LabelEncoder()
crop['label'] = label_encoder.fit_transform(crop['label'])

# Define features and target
X = crop.drop('label', axis=1)
y = crop['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Data Preprocessing
mx = MinMaxScaler()
X_train = mx.fit_transform(X_train)
X_test = mx.transform(X_test)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Initialize RandomForest model
randclf = RandomForestClassifier()
randclf.fit(X_train, y_train)

# Save the trained model to a file
model_path = 'random_forest_model.pkl'
joblib.dump(randclf, model_path)
print(f"Model saved to {model_path}")

# Evaluate model accuracy on test data
y_pred = randclf.predict(X_test)
print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Enhanced learning curve function with confidence intervals
def plot_learning_curve(estimator, X, y, cv, title="Learning Curve"):
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, scoring='accuracy', 
        n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10)
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, label="Training Accuracy", color="blue", marker='o')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15, color="blue")
    plt.plot(train_sizes, test_mean, label="Validation Accuracy", color="green", marker='o')
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.15, color="green")
    plt.title(title)
    plt.xlabel("Training Set Size")
    plt.ylabel("Accuracy")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()

# Validation curve for n_estimators
def plot_validation_curve():
    param_range = np.array([10, 30, 50, 70, 90, 110, 130, 150])
    train_scores, test_scores = validation_curve(
        RandomForestClassifier(), X, y, param_name="n_estimators",
        param_range=param_range, cv=5, scoring="accuracy", n_jobs=-1
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(param_range, train_mean, label="Training Score", color="darkorange", marker='o')
    plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, alpha=0.15, color="darkorange")
    plt.plot(param_range, test_mean, label="Cross-validation Score", color="navy", marker='o')
    plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, alpha=0.15, color="navy")
    plt.xlabel("Number of Trees")
    plt.ylabel("Accuracy Score")
    plt.title("Validation Curve")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()

# Enhanced noise testing with multiple noise levels
def test_noise_resistance(X_test, y_test, noise_levels=[0.1, 0.2, 0.3, 0.4, 0.5]):
    accuracies = []
    for noise_level in noise_levels:
        noisy_X = X_test + noise_level * np.random.normal(size=X_test.shape)
        noisy_pred = randclf.predict(noisy_X)
        acc = accuracy_score(y_test, noisy_pred)
        accuracies.append(acc)
        print(f"Accuracy with noise level {noise_level:.1f}: {acc:.4f}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(noise_levels, accuracies, marker='o')
    plt.xlabel("Noise Level")
    plt.ylabel("Accuracy")
    plt.title("Model Performance vs Noise Level")
    plt.grid(True)
    plt.show()

# Enhanced feature importance analysis
def analyze_feature_importance():
    # Get feature importance from Random Forest
    importances = randclf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in randclf.estimators_], axis=0)
    
    # Create DataFrame for visualization
    feature_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': importances,
        'Std': std
    }).sort_values('Importance', ascending=False)
    
    # Plot feature importances with error bars
    plt.figure(figsize=(10, 6))
    plt.errorbar(range(len(importances)), feature_importance_df['Importance'],
                yerr=feature_importance_df['Std'], fmt='o')
    plt.xticks(range(len(importances)), feature_importance_df['Feature'], rotation=45)
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title('Feature Importance with Variance')
    plt.tight_layout()
    plt.show()
    
    return feature_importance_df

# Plot confusion matrix
def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(12, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

# Run all validations
print("\n=== Running Comprehensive Model Validation ===")
print("\n1. Learning Curve Analysis")
plot_learning_curve(randclf, X, y, cv=5)

print("\n2. Validation Curve Analysis")
plot_validation_curve()

print("\n3. Noise Resistance Testing")
test_noise_resistance(X_test, y_test)

print("\n4. Feature Importance Analysis")
feature_importance_df = analyze_feature_importance()
print("\nFeature Importance Rankings:")
print(feature_importance_df)

print("\n5. Confusion Matrix")
plot_confusion_matrix(y_test, y_pred)

print("\n6. Detailed Classification Report")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Example usage with RandomForestClassifier
plot_learning_curve(randclf, X, y, cv=5, title="Learning Curve for RandomForestClassifier")

# Optional: K-fold cross-validation scores
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(randclf, X, y, cv=5)
print("\n7. Cross-validation Scores:")
print(f"CV Scores: {cv_scores}")
print(f"Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")