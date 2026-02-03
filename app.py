"""
Diabetes Prediction Web Application
AI-Based Diabetes Risk Prediction using Machine Learning
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
    .high-risk {
        background-color: #ffebee;
        border: 2px solid #ef5350;
    }
    .low-risk {
        background-color: #e8f5e9;
        border: 2px solid #66bb6a;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #2196f3;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the trained model and scaler"""
    try:
        with open('diabetes_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('model_info.pkl', 'rb') as f:
            model_info = pickle.load(f)
        return model, scaler, model_info
    except FileNotFoundError:
        return None, None, None

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability < 0.3:
        return "Low Risk", "#66bb6a", "😊"
    elif probability < 0.6:
        return "Medium Risk", "#ffa726", "😐"
    else:
        return "High Risk", "#ef5350", "😟"

def create_gauge_chart(probability):
    """Create a gauge chart for risk visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Diabetes Risk Score", 'font': {'size': 24}},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#e8f5e9'},
                {'range': [30, 60], 'color': '#fff3e0'},
                {'range': [60, 100], 'color': '#ffebee'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_feature_importance_chart(user_data):
    """Create a bar chart showing user's input values"""
    features = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 
                'Insulin', 'BMI', 'Pedigree Function', 'Age']
    values = list(user_data.values())
    
    fig = px.bar(
        x=features,
        y=values,
        labels={'x': 'Features', 'y': 'Values'},
        title='Your Health Parameters',
        color=values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    return fig

def provide_recommendations(prediction, user_data):
    """Provide health recommendations based on prediction and input"""
    recommendations = []
    
    if prediction == 1:
        recommendations.append("⚠️ **High Risk Detected**: Please consult a healthcare provider immediately for proper diagnosis.")
    
    # Glucose level recommendations
    if user_data['Glucose'] > 140:
        recommendations.append("🔴 **High Glucose Level**: Your glucose level is elevated. Consider dietary changes and consult a doctor.")
    elif user_data['Glucose'] > 100:
        recommendations.append("🟡 **Borderline Glucose**: Monitor your glucose levels regularly and maintain a healthy diet.")
    
    # BMI recommendations
    if user_data['BMI'] > 30:
        recommendations.append("🔴 **High BMI**: Your BMI indicates obesity. Weight management through diet and exercise is recommended.")
    elif user_data['BMI'] > 25:
        recommendations.append("🟡 **Overweight**: Consider lifestyle modifications to achieve a healthy weight.")
    
    # Blood Pressure recommendations
    if user_data['Blood Pressure'] > 90:
        recommendations.append("🔴 **High Blood Pressure**: Monitor your blood pressure regularly and reduce sodium intake.")
    
    # General recommendations
    if prediction == 1 or user_data['Glucose'] > 100 or user_data['BMI'] > 25:
        recommendations.append("✅ **Exercise**: Aim for at least 150 minutes of moderate aerobic activity per week.")
        recommendations.append("✅ **Diet**: Follow a balanced diet rich in vegetables, whole grains, and lean proteins.")
        recommendations.append("✅ **Monitoring**: Regular health check-ups and blood sugar monitoring are essential.")
    else:
        recommendations.append("✅ **Maintain**: Keep up your healthy lifestyle! Regular exercise and balanced diet are key.")
    
    return recommendations

def main():
    """Main application function"""
    
    # Header
    st.markdown('<p class="main-header">🏥 AI-Based Diabetes Prediction System</p>', unsafe_allow_html=True)
    
    # Load model
    model, scaler, model_info = load_model()
    
    if model is None:
        st.error("⚠️ Model not found! Please run 'train_model.py' first to train the model.")
        st.info("Run the following command in your terminal:\n```\npython train_model.py\n```")
        return
    
    # Sidebar - Model Information
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/stethoscope.png", width=100)
        st.title("About")
        st.info(
            "This application uses Machine Learning to predict diabetes risk "
            "based on medical and lifestyle parameters."
        )
        
        st.markdown("### Model Performance")
        st.metric("Model Used", model_info['model_name'])
        st.metric("Accuracy", f"{model_info['accuracy']*100:.2f}%")
        st.metric("Precision", f"{model_info['precision']*100:.2f}%")
        st.metric("Recall", f"{model_info['recall']*100:.2f}%")
        st.metric("F1-Score", f"{model_info['f1_score']*100:.2f}%")
        
        st.markdown("---")
        st.markdown("### How to Use")
        st.markdown(
            "1. Enter your health parameters\n"
            "2. Click 'Predict Risk'\n"
            "3. View your results and recommendations"
        )
        
        st.markdown("---")
        st.caption("⚠️ This is a prediction tool, not a diagnostic tool. Always consult healthcare professionals.")
    
    # Main content
    st.markdown("### 📋 Enter Your Health Information")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        pregnancies = st.number_input(
            "Number of Pregnancies",
            min_value=0,
            max_value=20,
            value=0,
            help="Number of times pregnant"
        )
        
        glucose = st.number_input(
            "Glucose Level (mg/dL)",
            min_value=0,
            max_value=300,
            value=120,
            help="Plasma glucose concentration (2 hours in an oral glucose tolerance test)"
        )
        
        blood_pressure = st.number_input(
            "Blood Pressure (mm Hg)",
            min_value=0,
            max_value=200,
            value=70,
            help="Diastolic blood pressure"
        )
        
        skin_thickness = st.number_input(
            "Skin Thickness (mm)",
            min_value=0,
            max_value=100,
            value=20,
            help="Triceps skin fold thickness"
        )
    
    with col2:
        insulin = st.number_input(
            "Insulin Level (mu U/ml)",
            min_value=0,
            max_value=900,
            value=80,
            help="2-Hour serum insulin"
        )
        
        bmi = st.number_input(
            "BMI (Body Mass Index)",
            min_value=0.0,
            max_value=110.0,
            value=25.0,
            step=0.1,
            help="Body mass index (weight in kg/(height in m)^2)"
        )
        
        dpf = st.number_input(
            "Diabetes Pedigree Function",
            min_value=0.0,
            max_value=3.0,
            value=0.5,
            step=0.01,
            help="Diabetes pedigree function (genetic influence)"
        )
        
        age = st.number_input(
            "Age (years)",
            min_value=1,
            max_value=120,
            value=30,
            help="Age in years"
        )
    
    # Predict button
    st.markdown("---")
    
    if st.button("🔮 Predict Diabetes Risk", use_container_width=True):
        # Prepare input data
        user_data = {
            'Pregnancies': pregnancies,
            'Glucose': glucose,
            'Blood Pressure': blood_pressure,
            'Skin Thickness': skin_thickness,
            'Insulin': insulin,
            'BMI': bmi,
            'Pedigree Function': dpf,
            'Age': age
        }
        
        # Create dataframe
        input_df = pd.DataFrame([list(user_data.values())], 
                                columns=['Pregnancies', 'Glucose', 'BloodPressure', 
                                        'SkinThickness', 'Insulin', 'BMI', 
                                        'DiabetesPedigreeFunction', 'Age'])
        
        # Scale input
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        
        # Display results
        st.markdown("---")
        st.markdown("## 📊 Prediction Results")
        
        # Create three columns for results
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Gauge chart
            st.plotly_chart(create_gauge_chart(probability), use_container_width=True)
        
        # Risk level
        risk_level, color, emoji = get_risk_level(probability)
        
        st.markdown(f"""
            <div class="prediction-box {'high-risk' if prediction == 1 else 'low-risk'}">
                <h2>{emoji} {risk_level}</h2>
                <h3>Probability: {probability*100:.2f}%</h3>
                <p style="font-size: 18px;">
                    {'You are at HIGH RISK of diabetes' if prediction == 1 else 'You are at LOW RISK of diabetes'}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature visualization
        st.markdown("### 📈 Your Health Parameters Overview")
        st.plotly_chart(create_feature_importance_chart(user_data), use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 Personalized Recommendations")
        recommendations = provide_recommendations(prediction, user_data)
        
        for rec in recommendations:
            st.markdown(f'<div class="info-box">{rec}</div>', unsafe_allow_html=True)
        
        # Download report option
        st.markdown("---")
        
        # Create report data
        report_data = {
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Risk Level': risk_level,
            'Probability': f"{probability*100:.2f}%",
            **user_data
        }
        
        report_df = pd.DataFrame([report_data])
        csv = report_df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv,
            file_name=f"diabetes_prediction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "Made with ❤️ for Healthcare | Minor Project 2025 | "
        "⚠️ For Educational Purposes Only - Not a Medical Diagnostic Tool"
        "</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
