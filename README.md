# 🏥 AI-Based Diabetes Prediction System

## Minor Project - Machine Learning Application

A complete web-based application for predicting diabetes risk using Machine Learning and Streamlit.

---

## 📋 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)

---

## ✨ Features

- **Multiple ML Models**: Compares 5 different algorithms (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, SVM)
- **Interactive Web Interface**: User-friendly Streamlit dashboard
- **Real-time Predictions**: Instant diabetes risk assessment
- **Risk Visualization**: Gauge charts and bar graphs
- **Personalized Recommendations**: Health advice based on input parameters
- **Report Download**: Export results as CSV
- **Model Performance Metrics**: Display accuracy, precision, recall, F1-score

---

## 🛠️ Technologies Used

### Backend
- Python 3.8+
- Scikit-learn (Machine Learning)
- Pandas & NumPy (Data Processing)
- Pickle (Model Serialization)

### Frontend
- Streamlit (Web Framework)
- Plotly (Interactive Visualizations)
- HTML/CSS (Custom Styling)

### Dataset
- Pima Indians Diabetes Dataset (UCI Machine Learning Repository)

---

## 📁 Project Structure

```
diabetes_prediction_app/
├── app.py                      # Main Streamlit application
├── train_model.py              # Model training script
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── diabetes_model.pkl          # Trained model (generated)
├── scaler.pkl                  # Feature scaler (generated)
└── model_info.pkl              # Model metadata (generated)
```

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <your-repo-url>
cd diabetes_prediction_app

# Or simply download and extract the folder
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the Model

```bash
python train_model.py
```

**Output**: You'll see model training progress and performance metrics. This will generate:
- `diabetes_model.pkl`
- `scaler.pkl`
- `model_info.pkl`

### Step 5: Run the Web Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

---

## 💻 Usage

### For Users

1. **Open the Application**: Navigate to `http://localhost:8501`

2. **Enter Health Parameters**:
   - Number of Pregnancies
   - Glucose Level (mg/dL)
   - Blood Pressure (mm Hg)
   - Skin Thickness (mm)
   - Insulin Level (mu U/ml)
   - BMI (Body Mass Index)
   - Diabetes Pedigree Function
   - Age (years)

3. **Get Prediction**: Click "Predict Diabetes Risk" button

4. **View Results**:
   - Risk level (Low/Medium/High)
   - Probability percentage
   - Visual gauge chart
   - Health parameters visualization
   - Personalized recommendations

5. **Download Report**: Export results as CSV file

---

## 🧠 Model Details

### Dataset Information
- **Source**: Pima Indians Diabetes Dataset
- **Samples**: 768 patients
- **Features**: 8 medical/lifestyle parameters
- **Target**: Binary (Diabetic: 1, Non-Diabetic: 0)

### Feature Descriptions

| Feature | Description | Unit |
|---------|-------------|------|
| Pregnancies | Number of times pregnant | count |
| Glucose | Plasma glucose concentration | mg/dL |
| Blood Pressure | Diastolic blood pressure | mm Hg |
| Skin Thickness | Triceps skin fold thickness | mm |
| Insulin | 2-Hour serum insulin | mu U/ml |
| BMI | Body mass index | kg/m² |
| Diabetes Pedigree Function | Genetic influence score | 0-3 |
| Age | Age of patient | years |

### Data Preprocessing

1. **Missing Value Handling**: Replace zeros with median values
2. **Feature Scaling**: StandardScaler normalization
3. **Train-Test Split**: 80-20 split with stratification
4. **Cross-Validation**: 5-fold CV for robust evaluation

### Models Trained

| Model | Typical Accuracy |
|-------|-----------------|
| Logistic Regression | 76-78% |
| Decision Tree | 70-73% |
| Random Forest | 75-78% |
| Gradient Boosting | 77-80% |
| SVM | 76-79% |

**Best Model Selection**: Based on highest F1-score

---

## 📸 Expected Output

### Model Training Output
```
================================================================================
DIABETES PREDICTION MODEL TRAINING
================================================================================

1. Loading data...
   Dataset shape: (768, 9)
   Diabetic cases: 268 (34.90%)

2. Preprocessing data...

3. Splitting data (80% train, 20% test)...

4. Scaling features...

5. Training models...
================================================================================
Logistic Regression:
  Accuracy:  0.7792
  Precision: 0.7234
  Recall:    0.6800
  F1-Score:  0.7010
  CV Score:  0.7719
--------------------------------------------------------------------------------
...

Best Model: Random Forest
F1-Score: 0.7458

Model, scaler, and info saved successfully!
```

### Web Application Features
- Clean, professional interface
- Interactive input forms
- Real-time risk calculation
- Color-coded risk levels (Green/Yellow/Red)
- Gauge chart visualization
- Bar chart of input parameters
- Personalized health recommendations
- CSV report download

---

## 🎯 Risk Classification

| Probability | Risk Level | Color | Action |
|-------------|-----------|-------|---------|
| 0-30% | Low Risk | Green 🟢 | Maintain healthy lifestyle |
| 30-60% | Medium Risk | Orange 🟡 | Monitor and improve habits |
| 60-100% | High Risk | Red 🔴 | Consult healthcare provider |

---

## 🔮 Future Enhancements

### Phase 1 (Easy)
- [ ] Add more visualizations (pie charts, histograms)
- [ ] Include BMI calculator
- [ ] Add data validation for inputs
- [ ] Implement session history

### Phase 2 (Medium)
- [ ] User authentication and profile storage
- [ ] Historical trend tracking
- [ ] Diet and exercise recommendations
- [ ] Integration with fitness trackers

### Phase 3 (Advanced)
- [ ] Deep Learning model (Neural Networks)
- [ ] Multi-disease prediction
- [ ] Doctor consultation booking
- [ ] Mobile app version
- [ ] Real-time glucose monitoring integration

---

## 📊 Project Report Structure

### For Academic Submission

**Chapter 1: Introduction**
- Background of diabetes
- Problem statement
- Objectives
- Scope and limitations

**Chapter 2: Literature Review**
- Existing systems
- Machine Learning in healthcare
- Related work analysis

**Chapter 3: System Design**
- System architecture
- Use case diagrams
- Flow charts
- Data flow diagrams

**Chapter 4: Implementation**
- Technologies used
- Algorithm explanation
- Code snippets
- Screenshots

**Chapter 5: Results and Discussion**
- Model performance comparison
- Accuracy metrics
- Confusion matrix
- ROC curves

**Chapter 6: Conclusion and Future Scope**
- Summary of findings
- Limitations
- Future enhancements

---

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Model files not found**
   ```bash
   python train_model.py
   ```

3. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

4. **Dataset download error**
   - Check internet connection
   - Try downloading dataset manually from UCI repository

---

## 📚 References

1. UCI Machine Learning Repository - Pima Indians Diabetes Dataset
2. Scikit-learn Documentation
3. Streamlit Documentation
4. World Health Organization (WHO) - Diabetes Statistics

---

## 👨‍💻 Author

**Your Name**
- College: [Your College Name]
- Department: [Your Department]
- Year: [Academic Year]
- Email: [Your Email]

---

## 📄 License

This project is for educational purposes only. Not intended for medical diagnosis.

---

## ⚠️ Disclaimer

This application is a **prediction tool**, not a diagnostic tool. The results should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions.

---

## 🙏 Acknowledgments

- Thanks to UCI Machine Learning Repository for the dataset
- Streamlit community for excellent documentation
- Scikit-learn developers for powerful ML tools

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Streamlit documentation
3. Contact project supervisor

---

**Made with ❤️ for Healthcare Education**
