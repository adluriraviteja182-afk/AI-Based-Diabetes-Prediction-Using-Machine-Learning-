"""
Enhanced Diabetes Prediction Web Application
Features:
- User accounts and login
- History tracking
- Multi-language support (English, Hindi, Telugu, Tamil)
- Better mobile optimization
- Data import suggestions
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import hashlib

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language translations
TRANSLATIONS = {
    'en': {
        'title': '🏥 AI-Based Diabetes Prediction System',
        'welcome': 'Welcome',
        'login': 'Login',
        'signup': 'Sign Up',
        'username': 'Username',
        'password': 'Password',
        'logout': 'Logout',
        'language': 'Language',
        'prediction_history': 'Prediction History',
        'new_prediction': 'New Prediction',
        'enter_health_info': '📋 Enter Your Health Information',
        'pregnancies': 'Number of Pregnancies',
        'glucose': 'Glucose Level (mg/dL)',
        'blood_pressure': 'Blood Pressure (mm Hg)',
        'skin_thickness': 'Skin Thickness (mm)',
        'insulin': 'Insulin Level (mu U/ml)',
        'bmi': 'BMI (Body Mass Index)',
        'pedigree': 'Diabetes Pedigree Function',
        'age': 'Age (years)',
        'predict_risk': '🔮 Predict Diabetes Risk',
        'prediction_results': '📊 Prediction Results',
        'low_risk': 'Low Risk',
        'medium_risk': 'Medium Risk',
        'high_risk': 'High Risk',
        'probability': 'Probability',
        'recommendations': '💡 Personalized Recommendations',
        'download_report': '📥 Download Report as CSV',
        'view_history': 'View Prediction History',
        'date': 'Date',
        'risk_level': 'Risk Level',
        'import_note': '📱 Note: For automatic data import from devices, connect your glucose monitor or fitness tracker to the system (feature coming soon)',
        'no_history': 'No prediction history yet. Make your first prediction!',
        'trend_chart': 'Risk Trend Over Time',
        'disclaimer': '⚠️ This is a screening tool, not a diagnostic device. Always consult healthcare professionals.',
    },
    'hi': {
        'title': '🏥 एआई-आधारित मधुमेह पूर्वानुमान प्रणाली',
        'welcome': 'स्वागत है',
        'login': 'लॉगिन',
        'signup': 'साइन अप',
        'username': 'उपयोगकर्ता नाम',
        'password': 'पासवर्ड',
        'logout': 'लॉगआउट',
        'language': 'भाषा',
        'prediction_history': 'पूर्वानुमान इतिहास',
        'new_prediction': 'नया पूर्वानुमान',
        'enter_health_info': '📋 अपनी स्वास्थ्य जानकारी दर्ज करें',
        'pregnancies': 'गर्भधारण की संख्या',
        'glucose': 'ग्लूकोज स्तर (mg/dL)',
        'blood_pressure': 'रक्तचाप (mm Hg)',
        'skin_thickness': 'त्वचा की मोटाई (mm)',
        'insulin': 'इंसुलिन स्तर (mu U/ml)',
        'bmi': 'बीएमआई (शरीर द्रव्यमान सूचकांक)',
        'pedigree': 'मधुमेह वंशावली कार्य',
        'age': 'आयु (वर्ष)',
        'predict_risk': '🔮 मधुमेह जोखिम की जांच करें',
        'prediction_results': '📊 पूर्वानुमान परिणाम',
        'low_risk': 'कम जोखिम',
        'medium_risk': 'मध्यम जोखिम',
        'high_risk': 'उच्च जोखिम',
        'probability': 'संभावना',
        'recommendations': '💡 व्यक्तिगत सिफारिशें',
        'download_report': '📥 सीएसवी के रूप में रिपोर्ट डाउनलोड करें',
        'view_history': 'पूर्वानुमान इतिहास देखें',
        'date': 'तारीख',
        'risk_level': 'जोखिम स्तर',
        'import_note': '📱 नोट: उपकरणों से स्वचालित डेटा आयात के लिए, अपने ग्लूकोज मॉनिटर या फिटनेस ट्रैकर को सिस्टम से कनेक्ट करें (सुविधा जल्द आ रही है)',
        'no_history': 'अभी तक कोई पूर्वानुमान इतिहास नहीं। अपना पहला पूर्वानुमान करें!',
        'trend_chart': 'समय के साथ जोखिम प्रवृत्ति',
        'disclaimer': '⚠️ यह एक स्क्रीनिंग उपकरण है, निदान उपकरण नहीं। हमेशा स्वास्थ्य पेशेवरों से परामर्श करें।',
    },
    'te': {
        'title': '🏥 AI-ఆధారిత మధుమేహ అంచనా వ్యవస్థ',
        'welcome': 'స్వాగతం',
        'login': 'లాగిన్',
        'signup': 'సైన్ అప్',
        'username': 'వినియోగదారు పేరు',
        'password': 'పాస్‌వర్డ్',
        'logout': 'లాగౌట్',
        'language': 'భాష',
        'prediction_history': 'అంచనా చరిత్ర',
        'new_prediction': 'కొత్త అంచనా',
        'enter_health_info': '📋 మీ ఆరోగ్య సమాచారాన్ని నమోదు చేయండి',
        'pregnancies': 'గర్భాల సంఖ్య',
        'glucose': 'గ్లూకోజ్ స్థాయి (mg/dL)',
        'blood_pressure': 'రక్తపోటు (mm Hg)',
        'skin_thickness': 'చర్మ మందం (mm)',
        'insulin': 'ఇన్సులిన్ స్థాయి (mu U/ml)',
        'bmi': 'BMI (శరీర ద్రవ్యరాశి సూచిక)',
        'pedigree': 'మధుమేహ వంశావళి విధి',
        'age': 'వయస్సు (సంవత్సరాలు)',
        'predict_risk': '🔮 మధుమేహ ప్రమాదాన్ని తనిఖీ చేయండి',
        'prediction_results': '📊 అంచనా ఫలితాలు',
        'low_risk': 'తక్కువ ప్రమాదం',
        'medium_risk': 'మధ్యస్థ ప్రమాదం',
        'high_risk': 'అధిక ప్రమాదం',
        'probability': 'సంభావ్యత',
        'recommendations': '💡 వ్యక్తిగత సిఫార్సులు',
        'download_report': '📥 CSV గా నివేదికను డౌన్‌లోడ్ చేయండి',
        'view_history': 'అంచనా చరిత్రను చూడండి',
        'date': 'తేదీ',
        'risk_level': 'ప్రమాద స్థాయి',
        'import_note': '📱 గమనిక: పరికరాల నుండి స్వయంచాలక డేటా దిగుమతి కోసం, మీ గ్లూకోజ్ మానిటర్ లేదా ఫిట్‌నెస్ ట్రాకర్‌ను సిస్టమ్‌కి కనెక్ట్ చేయండి (ఫీచర్ త్వరలో వస్తుంది)',
        'no_history': 'ఇంకా అంచనా చరిత్ర లేదు. మీ మొదటి అంచనా చేయండి!',
        'trend_chart': 'కాలక్రమంలో ప్రమాద ధోరణి',
        'disclaimer': '⚠️ ఇది స్క్రీనింగ్ సాధనం, రోగనిర్ధారణ పరికరం కాదు. ఎల్లప్పుడూ ఆరోగ్య నిపుణులను సంప్రదించండి.',
    },
    'ta': {
        'title': '🏥 AI-அடிப்படையிலான நீரிழிவு கணிப்பு அமைப்பு',
        'welcome': 'வரவேற்கிறோம்',
        'login': 'உள்நுழைய',
        'signup': 'பதிவு செய்க',
        'username': 'பயனர் பெயர்',
        'password': 'கடவுச்சொல்',
        'logout': 'வெளியேறு',
        'language': 'மொழி',
        'prediction_history': 'கணிப்பு வரலாறு',
        'new_prediction': 'புதிய கணிப்பு',
        'enter_health_info': '📋 உங்கள் சுகாதார தகவலை உள்ளிடவும்',
        'pregnancies': 'கர்ப்பங்களின் எண்ணிக்கை',
        'glucose': 'குளுக்கோஸ் அளவு (mg/dL)',
        'blood_pressure': 'இரத்த அழுத்தம் (mm Hg)',
        'skin_thickness': 'தோல் தடிமன் (mm)',
        'insulin': 'இன்சுலின் அளவு (mu U/ml)',
        'bmi': 'BMI (உடல் நிறை குறியீடு)',
        'pedigree': 'நீரிழிவு பரம்பரை செயல்பாடு',
        'age': 'வயது (ஆண்டுகள்)',
        'predict_risk': '🔮 நீரிழிவு ஆபத்தை சரிபார்க்கவும்',
        'prediction_results': '📊 கணிப்பு முடிவுகள்',
        'low_risk': 'குறைந்த ஆபத்து',
        'medium_risk': 'நடுத்தர ஆபத்து',
        'high_risk': 'அதிக ஆபத்து',
        'probability': 'நிகழ்தகவு',
        'recommendations': '💡 தனிப்பட்ட பரிந்துரைகள்',
        'download_report': '📥 CSV ஆக அறிக்கையை பதிவிறக்கவும்',
        'view_history': 'கணிப்பு வரலாற்றைக் காண்க',
        'date': 'தேதி',
        'risk_level': 'ஆபத்து நிலை',
        'import_note': '📱 குறிப்பு: சாதனங்களிலிருந்து தானியங்கி தரவு இறக்குமதிக்கு, உங்கள் குளுக்கோஸ் மானிட்டர் அல்லது பிட்னஸ் டிராக்கரை கணினியுடன் இணைக்கவும் (அம்சம் விரைவில் வரும்)',
        'no_history': 'இன்னும் கணிப்பு வரலாறு இல்லை. உங்கள் முதல் கணிப்பை செய்யுங்கள்!',
        'trend_chart': 'காலப்போக்கில் ஆபத்து போக்கு',
        'disclaimer': '⚠️ இது ஒரு திரையிடல் கருவி, கண்டறியும் சாதனம் அல்ல. எப்போதும் சுகாதார நிபுணர்களை அணுகவும்.',
    }
}

# User database file
USER_DB_FILE = 'users.json'
HISTORY_DB_FILE = 'prediction_history.json'

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
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

def load_users():
    """Load user database"""
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user database"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f)

def load_history():
    """Load prediction history"""
    if os.path.exists(HISTORY_DB_FILE):
        with open(HISTORY_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    """Save prediction history"""
    with open(HISTORY_DB_FILE, 'w') as f:
        json.dump(history, f)

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """Authenticate user"""
    users = load_users()
    if username in users:
        return users[username]['password'] == hash_password(password)
    return False

def create_user(username, password):
    """Create new user"""
    users = load_users()
    if username in users:
        return False
    users[username] = {'password': hash_password(password), 'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    save_users(users)
    return True

def add_prediction_to_history(username, prediction_data):
    """Add prediction to user's history"""
    history = load_history()
    if username not in history:
        history[username] = []
    
    history[username].append({
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data': prediction_data
    })
    save_history(history)

def get_user_history(username):
    """Get user's prediction history"""
    history = load_history()
    return history.get(username, [])

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

def get_risk_level(probability, lang='en'):
    """Determine risk level based on probability"""
    t = TRANSLATIONS[lang]
    if probability < 0.3:
        return t['low_risk'], "#66bb6a", "😊"
    elif probability < 0.6:
        return t['medium_risk'], "#ffa726", "😐"
    else:
        return t['high_risk'], "#ef5350", "😟"

def create_gauge_chart(probability):
    """Create a gauge chart for risk visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 24}},
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
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_history_chart(history_data):
    """Create trend chart from history"""
    if not history_data:
        return None
    
    dates = [item['date'] for item in history_data]
    probabilities = [item['data']['probability'] * 100 for item in history_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=probabilities,
        mode='lines+markers',
        name='Risk %',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Low Risk Threshold")
    fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
    
    fig.update_layout(
        title="Risk Trend Over Time",
        xaxis_title="Date",
        yaxis_title="Risk Probability (%)",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def login_page(lang='en'):
    """Login/Signup page"""
    t = TRANSLATIONS[lang]
    
    st.markdown(f'<p class="main-header">{t["title"]}</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs([t['login'], t['signup']])
    
    with tab1:
        st.subheader(t['login'])
        username = st.text_input(t['username'], key='login_username')
        password = st.text_input(t['password'], type='password', key='login_password')
        
        if st.button(t['login'], key='login_btn'):
            if authenticate(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error('❌ Invalid username or password')
    
    with tab2:
        st.subheader(t['signup'])
        new_username = st.text_input(t['username'], key='signup_username')
        new_password = st.text_input(t['password'], type='password', key='signup_password')
        confirm_password = st.text_input('Confirm Password', type='password', key='confirm_password')
        
        if st.button(t['signup'], key='signup_btn'):
            if not new_username or not new_password:
                st.error('❌ Please fill all fields')
            elif new_password != confirm_password:
                st.error('❌ Passwords do not match')
            elif len(new_password) < 6:
                st.error('❌ Password must be at least 6 characters')
            else:
                if create_user(new_username, new_password):
                    st.success('✅ Account created! Please login.')
                else:
                    st.error('❌ Username already exists')

def main_app(lang='en'):
    """Main application after login"""
    t = TRANSLATIONS[lang]
    
    # Header
    st.markdown(f'<p class="main-header">{t["title"]}</p>', unsafe_allow_html=True)
    
    # Load model
    model, scaler, model_info = load_model()
    
    if model is None:
        st.error("⚠️ Model not found! Please run 'train_model_offline.py' first.")
        return
    
    # Sidebar
    with st.sidebar:
        st.write(f"### {t['welcome']}, {st.session_state['username']}! 👋")
        
        if st.button(t['logout']):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### Model Performance")
        st.metric("Model", model_info['model_name'])
        st.metric("Accuracy", f"{model_info['accuracy']*100:.2f}%")
        st.metric("F1-Score", f"{model_info['f1_score']*100:.2f}%")
        
        st.markdown("---")
        
        page = st.radio("Navigation", [t['new_prediction'], t['view_history']])
    
    if page == t['new_prediction']:
        # New prediction page
        st.markdown(f"### {t['enter_health_info']}")
        
        # Data import note
        st.info(t['import_note'])
        
        # Create two columns for input
        col1, col2 = st.columns(2)
        
        with col1:
            pregnancies = st.number_input(t['pregnancies'], min_value=0, max_value=20, value=0)
            glucose = st.number_input(t['glucose'], min_value=0, max_value=300, value=120)
            blood_pressure = st.number_input(t['blood_pressure'], min_value=0, max_value=200, value=70)
            skin_thickness = st.number_input(t['skin_thickness'], min_value=0, max_value=100, value=20)
        
        with col2:
            insulin = st.number_input(t['insulin'], min_value=0, max_value=900, value=80)
            bmi = st.number_input(t['bmi'], min_value=0.0, max_value=110.0, value=25.0, step=0.1)
            dpf = st.number_input(t['pedigree'], min_value=0.0, max_value=3.0, value=0.5, step=0.01)
            age = st.number_input(t['age'], min_value=1, max_value=120, value=30)
        
        # Predict button
        st.markdown("---")
        
        if st.button(t['predict_risk'], use_container_width=True):
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
            
            # Save to history
            prediction_data = {
                'prediction': int(prediction),
                'probability': float(probability),
                'inputs': user_data
            }
            add_prediction_to_history(st.session_state['username'], prediction_data)
            
            # Display results
            st.markdown("---")
            st.markdown(f"## {t['prediction_results']}")
            
            # Gauge chart
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.plotly_chart(create_gauge_chart(probability), use_container_width=True)
            
            # Risk level
            risk_level, color, emoji = get_risk_level(probability, lang)
            
            st.markdown(f"""
                <div class="prediction-box {'high-risk' if prediction == 1 else 'low-risk'}">
                    <h2>{emoji} {risk_level}</h2>
                    <h3>{t['probability']}: {probability*100:.2f}%</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Recommendations
            st.markdown(f"### {t['recommendations']}")
            
            if prediction == 1:
                st.markdown(f'<div class="info-box">⚠️ High risk detected. Please consult a healthcare provider immediately.</div>', unsafe_allow_html=True)
                
                # DETAILED DIET PLAN FOR DIABETIC PATIENTS
                st.markdown("---")
                st.markdown("### 🥗 **Recommended Diet Plan for Diabetes Management**")
                
                st.markdown("#### ✅ **Foods to EAT:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    **🥬 Vegetables (Unlimited):**
                    - Leafy greens: Spinach, kale, methi (fenugreek)
                    - Broccoli, cauliflower, cabbage
                    - Tomatoes, cucumber, capsicum
                    - Bitter gourd (karela) - excellent for diabetes
                    - Ridge gourd, bottle gourd, pumpkin
                    
                    **🍎 Fruits (Limited portions):**
                    - Berries: Strawberries, blueberries
                    - Apple (1 small/day)
                    - Guava, papaya
                    - Orange (1 small/day)
                    - **Avoid:** Mango, banana, grapes (high sugar)
                    
                    **🌾 Whole Grains:**
                    - Brown rice (instead of white rice)
                    - Whole wheat roti
                    - Oats, quinoa
                    - Millets: Ragi, bajra, jowar
                    - **Limit:** White rice, maida (refined flour)
                    """)
                
                with col2:
                    st.markdown("""
                    **🥜 Proteins:**
                    - Lentils: Moong dal, masoor dal
                    - Chickpeas, kidney beans
                    - Fish (salmon, mackerel) - 2-3 times/week
                    - Chicken (skinless, grilled)
                    - Eggs (boiled)
                    - Paneer (cottage cheese) - in moderation
                    - Tofu, soya
                    
                    **🥛 Dairy:**
                    - Low-fat milk
                    - Plain curd (yogurt)
                    - Buttermilk (chaas)
                    - **Limit:** Full-fat milk, cheese
                    
                    **🥤 Beverages:**
                    - Water (8-10 glasses/day)
                    - Green tea (unsweetened)
                    - Herbal teas
                    - Buttermilk
                    - **Avoid:** Sugary drinks, soda, packaged juices
                    """)
                
                st.markdown("---")
                st.markdown("#### ❌ **Foods to AVOID:**")
                
                st.markdown("""
                <div style="background-color: #ffebee; padding: 15px; border-radius: 10px; border-left: 5px solid #ef5350;">
                
                **🚫 High Sugar Foods:**
                - White sugar, jaggery (limit)
                - Sweets, candies, chocolates
                - Ice cream, pastries, cakes
                - Sweetened beverages, soft drinks
                - Honey (in excess)
                
                **🚫 Refined Carbohydrates:**
                - White bread, maida products
                - White rice (prefer brown rice)
                - Pasta (refined), noodles
                - Biscuits, cookies
                - Packaged snacks, chips
                
                **🚫 Fried & Processed Foods:**
                - Deep-fried foods (samosa, pakora, puri)
                - Fast food (pizza, burger, fries)
                - Processed meats (sausages, salami)
                - Trans fats, vanaspati
                
                **🚫 High-Fat Foods:**
                - Full-fat dairy products
                - Fatty cuts of meat
                - Coconut oil in excess
                - Butter, ghee (limit to 1-2 tsp/day)
                
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 🍽️ **Sample Daily Meal Plan**")
                
                meal_col1, meal_col2, meal_col3 = st.columns(3)
                
                with meal_col1:
                    st.markdown("""
                    **🌅 Breakfast (7-8 AM):**
                    - 2 wheat rotis + vegetable curry
                    OR
                    - 1 bowl oats + nuts
                    OR
                    - 2 boiled eggs + 1 toast
                    - 1 cup green tea (no sugar)
                    
                    **☕ Mid-Morning (10-11 AM):**
                    - 1 fruit (apple/guava)
                    OR
                    - Handful of nuts (almonds/walnuts)
                    - Buttermilk
                    """)
                
                with meal_col2:
                    st.markdown("""
                    **🍛 Lunch (12-1 PM):**
                    - 1-2 rotis (whole wheat)
                    - 1 bowl dal (lentils)
                    - 1 bowl vegetable curry
                    - Salad (unlimited)
                    - 1 cup curd
                    - **Avoid:** White rice or limit to ½ cup
                    
                    **🥤 Evening (4-5 PM):**
                    - Green tea + roasted chana
                    OR
                    - Sprouts salad
                    OR
                    - Vegetable soup
                    """)
                
                with meal_col3:
                    st.markdown("""
                    **🌙 Dinner (7-8 PM):**
                    - 1-2 rotis
                    - Grilled chicken/fish OR dal
                    - 1 bowl vegetables
                    - Salad
                    - **Early dinner:** Before 8 PM
                    
                    **🛏️ Before Bed:**
                    - 1 cup warm milk (low-fat)
                    - **Avoid:** Late-night snacking
                    """)
                
                st.markdown("---")
                st.markdown("### 🏃 **Recommended Exercise Plan**")
                
                st.markdown("""
                <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 5px solid #66bb6a;">
                
                **⏰ Goal:** At least 150 minutes per week (30 min/day × 5 days)
                
                </div>
                """, unsafe_allow_html=True)
                
                ex_col1, ex_col2 = st.columns(2)
                
                with ex_col1:
                    st.markdown("""
                    **🚶 Aerobic Exercises (Daily):**
                    - **Walking:** 30-45 minutes brisk walk
                      - Best: Morning or evening
                      - After meals helps reduce blood sugar
                    - **Jogging/Running:** 20-30 minutes
                    - **Cycling:** 30-45 minutes
                    - **Swimming:** 30 minutes
                    - **Dancing:** 30 minutes
                    
                    **💪 Strength Training (3x/week):**
                    - Weight lifting (light weights)
                    - Resistance bands
                    - Push-ups, squats, lunges
                    - Core exercises
                    - **Duration:** 20-30 minutes
                    
                    **🧘 Flexibility (Daily):**
                    - Yoga: 20-30 minutes
                    - Stretching: 10-15 minutes
                    - Pranayama (breathing exercises)
                    """)
                
                with ex_col2:
                    st.markdown("""
                    **📅 Weekly Exercise Schedule:**
                    
                    **Monday:** 30 min walk + 20 min strength
                    **Tuesday:** 30 min cycling/jogging
                    **Wednesday:** 30 min walk + 20 min yoga
                    **Thursday:** 30 min swimming/dancing
                    **Friday:** 30 min walk + 20 min strength
                    **Saturday:** 45 min brisk walk
                    **Sunday:** 30 min yoga/stretching (light)
                    
                    **⚠️ Important Tips:**
                    - Start slowly, increase gradually
                    - Check blood sugar before exercise
                    - Carry glucose tablets (low sugar emergency)
                    - Wear comfortable shoes
                    - Stay hydrated
                    - Exercise at same time daily
                    - **Best time:** 30-60 min after meals
                    """)
                
                st.markdown("---")
                st.markdown("### 📋 **Additional Lifestyle Tips**")
                
                st.markdown("""
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px;">
                
                **✅ Do's:**
                - Monitor blood sugar regularly (before meals, 2 hours after meals)
                - Eat small, frequent meals (5-6 times/day)
                - Drink 8-10 glasses of water daily
                - Sleep 7-8 hours/night
                - Manage stress (meditation, yoga)
                - Check feet daily for cuts/sores
                - Regular health check-ups (every 3 months)
                - Take medications on time
                - Carry diabetic ID card
                
                **❌ Don'ts:**
                - Skip meals (causes blood sugar fluctuations)
                - Smoke (increases complications)
                - Drink alcohol (or limit strictly)
                - Sit for long periods (move every 30 min)
                - Ignore symptoms (thirst, frequent urination, fatigue)
                - Self-medicate
                - Delay doctor visits
                
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 📞 **When to Contact Doctor IMMEDIATELY:**")
                
                st.markdown("""
                <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px; border-left: 5px solid #ffa726;">
                
                **🚨 Emergency Signs:**
                - Blood sugar below 70 mg/dL (hypoglycemia)
                - Blood sugar above 300 mg/dL (hyperglycemia)
                - Severe dizziness or confusion
                - Excessive thirst/urination
                - Blurred vision
                - Chest pain
                - Difficulty breathing
                - Numbness in feet/hands
                - Non-healing wounds
                
                **Emergency Contacts:**
                - Keep doctor's number handy
                - Know nearest hospital location
                - Inform family about condition
                
                </div>
                """, unsafe_allow_html=True)
            
            # GENERAL RECOMMENDATIONS (even for low/medium risk)
            if glucose > 140:
                st.markdown(f'<div class="info-box">🔴 High glucose level detected. Reduce sugar intake and consult a doctor.</div>', unsafe_allow_html=True)
            
            if bmi > 30:
                st.markdown(f'<div class="info-box">🔴 BMI indicates obesity. Weight management through diet and exercise is recommended.</div>', unsafe_allow_html=True)
                st.markdown("**Weight Loss Tips:** Aim to lose 5-10% of body weight through diet + exercise. Even small weight loss significantly reduces diabetes risk.")
            elif bmi > 25:
                st.markdown(f'<div class="info-box">🟡 Overweight. Consider lifestyle modifications to achieve a healthy weight.</div>', unsafe_allow_html=True)
            
            if blood_pressure > 90:
                st.markdown(f'<div class="info-box">🔴 High blood pressure detected. Monitor regularly and reduce sodium intake.</div>', unsafe_allow_html=True)
            
            # Basic recommendations for everyone
            if prediction == 0:  # Low risk patients also get basic tips
                st.markdown("---")
                st.markdown("### ✅ **Maintain Your Healthy Lifestyle:**")
                st.markdown("""
                - Continue balanced diet with whole grains, vegetables, lean proteins
                - Exercise 150 minutes/week (30 min × 5 days)
                - Maintain healthy weight (BMI 18.5-24.9)
                - Regular health check-ups annually
                - Manage stress through yoga/meditation
                - Avoid smoking and limit alcohol
                - Sleep 7-8 hours/night
                """)
            
            st.markdown(f'<div class="info-box">✅ Exercise: Aim for at least 150 minutes of moderate aerobic activity per week.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box">✅ Diet: Follow a balanced diet rich in vegetables, whole grains, and lean proteins.</div>', unsafe_allow_html=True)
            
            # Download report
            st.markdown("---")
            report_data = {
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Username': st.session_state['username'],
                'Risk Level': risk_level,
                'Probability': f"{probability*100:.2f}%",
                **user_data
            }
            report_df = pd.DataFrame([report_data])
            csv = report_df.to_csv(index=False)
            
            st.download_button(
                label=t['download_report'],
                data=csv,
                file_name=f"diabetes_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    else:
        # History page
        st.markdown(f"### {t['prediction_history']}")
        
        history = get_user_history(st.session_state['username'])
        
        if not history:
            st.info(t['no_history'])
        else:
            # Show trend chart
            st.markdown(f"#### {t['trend_chart']}")
            fig = create_history_chart(history)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Show history table
            st.markdown("---")
            st.markdown("#### Detailed History")
            
            history_data = []
            for item in reversed(history):  # Most recent first
                date = item['date']
                prob = item['data']['probability']
                risk_level, _, emoji = get_risk_level(prob, lang)
                
                history_data.append({
                    t['date']: date,
                    t['risk_level']: f"{emoji} {risk_level}",
                    t['probability']: f"{prob*100:.2f}%",
                    'Glucose': item['data']['inputs']['Glucose'],
                    'BMI': item['data']['inputs']['BMI'],
                    'Age': item['data']['inputs']['Age']
                })
            
            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df, use_container_width=True)
            
            # Download full history
            full_csv = history_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full History",
                data=full_csv,
                file_name=f"prediction_history_{st.session_state['username']}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<p style='text-align: center; color: gray;'>{t['disclaimer']}</p>",
        unsafe_allow_html=True
    )

def main():
    """Main application entry point"""
    # Initialize session state FIRST - before anything else
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'  # ← Initialize BEFORE sidebar
    
    # Language selector in sidebar
    with st.sidebar:
        lang_options = {
            'en': 'English',
            'hi': 'हिन्दी (Hindi)',
            'te': 'తెలుగు (Telugu)',
            'ta': 'தமிழ் (Tamil)'
        }
        selected_lang = st.selectbox(
            "🌐 Language / भाषा / భాష / மொழி",
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=list(lang_options.keys()).index(st.session_state['language'])
        )
        
        if selected_lang != st.session_state['language']:
            st.session_state['language'] = selected_lang
            st.rerun()
    
    lang = st.session_state['language']
    
    # Route to appropriate page
    if not st.session_state['logged_in']:
        login_page(lang)
    else:
        main_app(lang)