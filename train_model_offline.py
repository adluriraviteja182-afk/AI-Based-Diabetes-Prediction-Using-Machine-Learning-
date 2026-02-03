"""
Diabetes Prediction Model Training - Alternative Version
This script includes sample data for offline training
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import warnings
warnings.filterwarnings('ignore')

# Sample Pima Indians Diabetes Dataset (first 100 rows as example)
SAMPLE_DATA = """6,148,72,35,0,33.6,0.627,50,1
1,85,66,29,0,26.6,0.351,31,0
8,183,64,0,0,23.3,0.672,32,1
1,89,66,23,94,28.1,0.167,21,0
0,137,40,35,168,43.1,2.288,33,1
5,116,74,0,0,25.6,0.201,30,0
3,78,50,32,88,31.0,0.248,26,1
10,115,0,0,0,35.3,0.134,29,0
2,197,70,45,543,30.5,0.158,53,1
8,125,96,0,0,0.0,0.232,54,1
4,110,92,0,0,37.6,0.191,30,0
10,168,74,0,0,38.0,0.537,34,1
10,139,80,0,0,27.1,1.441,57,0
1,189,60,23,846,30.1,0.398,59,1
5,166,72,19,175,25.8,0.587,51,1
7,100,0,0,0,30.0,0.484,32,1
0,118,84,47,230,45.8,0.551,31,1
7,107,74,0,0,29.6,0.254,31,1
1,103,30,38,83,43.3,0.183,33,0
1,115,70,30,96,34.6,0.529,32,1
3,126,88,41,235,39.3,0.704,27,0
8,99,84,0,0,35.4,0.388,50,0
7,196,90,0,0,39.8,0.451,41,1
9,119,80,35,0,29.0,0.263,29,1
11,143,94,33,146,36.6,0.254,51,1
10,125,70,26,115,31.1,0.205,41,1
7,147,76,0,0,39.4,0.257,43,1
1,97,66,15,140,23.2,0.487,22,0
13,145,82,19,110,22.2,0.245,57,0
5,117,92,0,0,34.1,0.337,38,0
5,109,75,26,0,36.0,0.546,60,0
3,158,76,36,245,31.6,0.851,28,1
3,88,58,11,54,24.8,0.267,22,0
6,92,92,0,0,19.9,0.188,28,0
10,122,78,31,0,27.6,0.512,45,0
4,103,60,33,192,24.0,0.966,33,0
11,138,76,0,0,33.2,0.420,35,0
9,102,76,37,0,32.9,0.665,46,1
2,90,68,42,0,38.2,0.503,27,1
4,111,72,47,207,37.1,1.390,56,1
3,180,64,25,70,34.0,0.271,26,0
7,133,84,0,0,40.2,0.696,37,0
7,106,92,18,0,22.7,0.235,48,0
9,171,110,24,240,45.4,0.721,54,1
7,159,64,0,0,27.4,0.294,40,0
0,180,66,39,0,42.0,1.893,25,1
1,146,56,0,0,29.7,0.564,29,0
2,71,70,27,0,28.0,0.586,22,0
7,103,66,32,0,39.1,0.344,31,1
7,105,0,0,0,0.0,0.305,24,0
1,103,80,11,82,19.4,0.491,22,0
1,101,50,15,36,24.2,0.526,26,0
5,88,66,21,23,24.4,0.342,30,0
8,176,90,34,300,33.7,0.467,58,1
7,150,66,42,342,34.7,0.718,42,0
1,73,50,10,0,23.0,0.248,21,0
7,187,68,39,304,37.7,0.254,41,1
0,100,88,60,110,46.8,0.962,31,0
0,146,82,0,0,40.5,1.781,44,0
0,105,64,41,142,41.5,0.173,22,0
2,84,0,0,0,0.0,0.304,21,0
8,133,72,0,0,32.9,0.270,39,1
5,44,62,0,0,25.0,0.587,36,0
2,141,58,34,128,25.4,0.699,24,0
7,114,66,0,0,32.8,0.258,42,1
5,99,74,27,0,29.0,0.203,32,0
0,109,88,30,0,32.5,0.855,38,1
2,109,92,0,0,42.7,0.845,54,0
1,95,66,13,38,19.6,0.334,25,0
4,146,85,27,100,28.9,0.189,27,0
2,100,66,20,90,32.9,0.867,28,1
5,139,64,35,140,28.6,0.411,26,0
13,126,90,0,0,43.4,0.583,42,1
4,129,86,20,270,35.1,0.231,23,0
1,79,75,30,0,32.0,0.396,22,0
1,0,48,20,0,24.7,0.140,22,0
7,62,78,0,0,32.6,0.391,41,0
5,95,72,33,0,37.7,0.370,27,0
0,131,0,0,0,43.2,0.270,26,1
2,112,66,22,0,25.0,0.307,24,0
3,113,44,13,0,22.4,0.140,22,0
2,74,0,0,0,0.0,0.102,22,0
7,83,78,26,71,29.3,0.767,36,0
0,101,65,28,0,24.6,0.237,22,0
5,137,108,0,0,48.8,0.227,37,1
2,110,74,29,125,32.4,0.698,27,0
13,106,72,54,0,36.6,0.178,45,0
2,100,68,25,71,38.5,0.324,26,0
15,136,70,32,110,37.1,0.153,43,1
1,107,68,19,0,26.5,0.165,24,0
1,80,55,0,0,19.1,0.258,21,0
4,123,80,15,176,32.0,0.443,34,0
7,81,78,40,48,46.7,0.261,42,0
4,134,72,0,0,23.8,0.277,60,1
2,142,82,18,64,24.7,0.761,21,0
6,144,72,27,228,33.9,0.255,40,0
2,92,62,28,0,31.6,0.130,24,0
1,71,48,18,76,20.4,0.323,22,0
6,93,50,30,64,28.7,0.356,23,0"""

def create_sample_dataset():
    """Create dataset from sample data"""
    from io import StringIO
    
    columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
               'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    
    df = pd.read_csv(StringIO(SAMPLE_DATA), names=columns)
    return df

def load_data():
    """Load the Pima Indians Diabetes Dataset"""
    print("   Loading sample dataset...")
    df = create_sample_dataset()
    
    # If you have internet, you can uncomment this to download full dataset:
    # url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    # df = pd.read_csv(url, names=columns)
    
    return df

def preprocess_data(df):
    """Clean and preprocess the data"""
    # Replace zeros with NaN for specific columns
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
        'SVM': SVC(kernel='rbf', random_state=42, probability=True)
    }
    
    results = {}
    
    print("\nTraining and evaluating models...\n")
    print("=" * 80)
    
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=3)
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
    print("Files created: diabetes_model.pkl, scaler.pkl, model_info.pkl")
    
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
    print("\nNext steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open browser to http://localhost:8501")
    print("3. Start making predictions!")

if __name__ == "__main__":
    main()
