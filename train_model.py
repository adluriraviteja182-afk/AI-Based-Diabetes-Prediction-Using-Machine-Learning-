"""
Diabetes Prediction Model Training
This script trains multiple ML models and saves the best one
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import pickle
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load the Pima Indians Diabetes Dataset"""
    # Dataset URL
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    
    # Column names
    columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
               'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    
    # Load data
    df = pd.read_csv(url, names=columns)
    return df

def preprocess_data(df):
    """Clean and preprocess the data"""
    # Replace zeros with NaN for specific columns (zeros are impossible values)
    zero_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[zero_columns] = df[zero_columns].replace(0, np.nan)
    
    # Fill missing values with median
    df.fillna(df.median(), inplace=True)
    
    # Separate features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    return X, y

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and compare performance"""
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'SVM': SVC(kernel='rbf', random_state=42)
    }
    
    results = {}
    
    print("Training and evaluating models...\n")
    print("=" * 80)
    
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        cv_mean = cv_scores.mean()
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_score': cv_mean
        }
        
        print(f"{name}:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  CV Score:  {cv_mean:.4f}")
        print("-" * 80)
    
    return results

def save_best_model(results, scaler):
    """Save the best performing model"""
    # Find best model based on F1-score
    best_model_name = max(results, key=lambda x: results[x]['f1_score'])
    best_model = results[best_model_name]['model']
    
    print(f"\nBest Model: {best_model_name}")
    print(f"F1-Score: {results[best_model_name]['f1_score']:.4f}")
    
    # Save model and scaler
    with open('diabetes_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Save model info
    model_info = {
        'model_name': best_model_name,
        'accuracy': results[best_model_name]['accuracy'],
        'precision': results[best_model_name]['precision'],
        'recall': results[best_model_name]['recall'],
        'f1_score': results[best_model_name]['f1_score'],
        'cv_score': results[best_model_name]['cv_score']
    }
    
    with open('model_info.pkl', 'wb') as f:
        pickle.dump(model_info, f)
    
    print("\nModel, scaler, and info saved successfully!")
    
    return best_model_name, best_model

def main():
    """Main execution function"""
    print("=" * 80)
    print("DIABETES PREDICTION MODEL TRAINING")
    print("=" * 80)
    
    # Load data
    print("\n1. Loading data...")
    df = load_data()
    print(f"   Dataset shape: {df.shape}")
    print(f"   Diabetic cases: {df['Outcome'].sum()} ({df['Outcome'].mean()*100:.2f}%)")
    
    # Preprocess data
    print("\n2. Preprocessing data...")
    X, y = preprocess_data(df)
    
    # Split data
    print("\n3. Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    print("\n4. Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models
    print("\n5. Training models...")
    results = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Save best model
    print("\n6. Saving best model...")
    save_best_model(results, scaler)
    
    print("\n" + "=" * 80)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
