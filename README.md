# 🧠 MindScore AI — Student Mental Health & Digital Wellbeing Intelligence Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://naren1122-ml-mental-health-score-frontendapp-unguti.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-EB5424?logo=xgboost&logoColor=white)](https://xgboost.ai/)
[![Code Style: Clean](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/Naren1122/ML_mental_health_score)

---

### 🌐 Live Links & Demos
* **🚀 Live Interactive Application:** [Launch MindScore Streamlit App](https://naren1122-ml-mental-health-score-frontendapp-unguti.streamlit.app/)
* **💻 Source Code & Repository:** [GitHub: Naren1122/ML_mental_health_score](https://github.com/Naren1122/ML_mental_health_score)

---

## 📌 Executive Summary

**MindScore AI** is an end-to-end Machine Learning web platform designed to analyze, benchmark, and predict student mental wellbeing scores based on digital lifestyle indicators, circadian health, physical activity, and academic routines.

Traditional psychometric assessments rely on subjective self-reporting that often fails to quantify the compounding impact of digital overuse and fragmented attention. MindScore bridges this gap by training **5 distinct regression algorithms** on a 5,000-student cross-national dataset, surfacing granular lifestyle drivers through an asynchronous **FastAPI** backend and an intuitive, glassmorphic **Streamlit** dashboard.

### 🌟 Key Highlights
- **Ensemble Regression Suite:** 5 algorithms trained and benchmarked side-by-side: **Random Forest** ($R^2 = 0.8791$), **KNN** ($R^2 = 0.8400$), **XGBoost** ($R^2 = 0.8284$), **SVR** ($R^2 = 0.8072$), and **Linear Regression** ($R^2 = 0.7398$).
- **End-to-End Production Architecture:** Decoupled client-server design featuring a RESTful **FastAPI** microservice communicating via typed **Pydantic v2** payloads with a rich **Streamlit** frontend.
- **Explainable & Actionable Insights:** Integrated dynamic correlation matrix and an automated heuristic recommendation engine delivering evidence-based digital hygiene protocols.
- **Robust Pipeline Engineering:** Fully encapsulated scikit-learn `Pipeline` objects with `ColumnTransformer` handling log transformations, ordinal encodings, and one-hot encoding without data leakage.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph ClientLayer ["🖥️ Frontend Layer (Streamlit Cloud)"]
        UI["Modern Glassmorphic UI"]
        InputForm["Student Lifestyle Inputs\n(Screen Time, Sleep, Unlocks, Study)"]
        Heatmap["Exploratory Correlation Matrix"]
        MultiCompare["Multi-Model Benchmark Chart"]
    end

    subgraph APILayer ["⚡ Backend API Layer (FastAPI Microservice)"]
        FastAPIApp["FastAPI Service (Uvicorn)"]
        Lifespan["Async Lifespan Engine (Preloads Models in Memory)"]
        Validation["Pydantic v2 Feature Validation & Schema Guard"]
        Endpoints["/predict (Single Model)\n/predict/all (Multi-Model)\n/health (Liveness)"]
    end

    subgraph MLEngine ["🤖 Machine Learning Inference Engine"]
        Preprocessor["ColumnTransformer Pipeline\n• Log1p & Scaler (Study Hours)\n• StandardScaler (Numeric Features)\n• OrdinalEncoder (Stress Level)\n• OneHotEncoder (Categoricals)"]
        RF["🌲 Random Forest (Best R²: 0.88)"]
        XGB["🚀 XGBoost Regressor"]
        KNN["🎯 K-Nearest Neighbors"]
        SVR_M["⚙️ Support Vector Regressor"]
        LR["📈 Linear Regression"]
    end

    InputForm -->|HTTP POST JSON| Validation
    Validation --> FastAPIApp
    Lifespan --> Preprocessor
    FastAPIApp --> Preprocessor
    Preprocessor --> RF & XGB & KNN & SVR_M & LR
    RF & XGB & KNN & SVR_M & LR -->|Inference Score (1.0 - 10.0)| Endpoints
    Endpoints -->|Clamped Score + Category + Actionable Protocols| UI
    UI --> MultiCompare & Heatmap
```

---

## 📊 Dataset & Statistical Findings

The models are trained on a comprehensive study of **5,000 university and secondary school students** across 10+ countries exploring the behavioral intersection of digital habits, academic engagement, and mental health.

### Target Variable: `Mental_Health_Score`
* **Scale:** Continuous index from `1.0` (Severe Psychological Distress) to `10.0` (Flourishing / High Equilibrium).
* **Mean:** `6.23 ± 1.28` (Median: `6.20`).
* **Categorical Brackets:**
  * 🟢 `8.0 – 10.0`: Resilient & Thriving
  * 🔵 `6.5 – 7.9`: Balanced & Healthy
  * 🟠 `5.0 – 6.4`: Mild Distress / Elevated Stress
  * 🔴 `1.0 – 4.9`: Critical Distress / High Risk

### Key Empirical Correlations with Mental Wellbeing
| Feature | Type | Correlation ($r$) | Psychological Impact |
| :--- | :--- | :---: | :--- |
| **`Sleep_Hours_Per_Night`** | Continuous | **+0.766** | Strongest positive protective factor for emotional resilience |
| **`Study_Hours`** | Continuous | **+0.753** | Positive correlation with sense of purpose and academic efficacy |
| **`Physical_Activity_Hours`** | Continuous | **+0.521** | Moderate positive buffer against cognitive fatigue |
| **`Daily_Unlocks`** | Integer | **-0.791** | High unlocks (>180/day) indicate chronic task-switching and attention fragmentation |
| **`Avg_Daily_Usage_Hours`** | Continuous | **-0.816** | Strongest negative drag on emotional stability when >6 hrs/day |

---

## 🔬 Model Benchmarking & Performance

All 5 models were evaluated on an independent 30% holdout test set ($N = 1,500$) using identical preprocessing pipelines:

| Model Architecture | $R^2$ Score (Variance Explained) | Root Mean Squared Error (RMSE) | Mean Absolute Error (MAE) | Ranking |
| :--- | :---: | :---: | :---: | :---: |
| 🌲 **Random Forest Regressor** | **0.8791** | **0.4608** | **0.3452** | 🥇 **Best Overall** |
| 🎯 **K-Nearest Neighbors (KNN)** | **0.8400** | **0.5301** | **0.3836** | 🥈 High Accuracy |
| 🚀 **XGBoost Regressor** | **0.8284** | **0.5490** | **0.4274** | 🥉 Gradient Boosted |
| ⚙️ **Support Vector Regressor (SVR)** | **0.8072** | **0.5820** | **0.4361** | Kernel Non-linear |
| 📈 **Linear Regression** | **0.7398** | **0.6760** | **0.5362** | Baseline Benchmark |

### Why Random Forest Outperformed
The non-linear interactions between heavy phone unlocks, diminished sleep, and subjective stress levels contain complex decision thresholds that tree-based ensemble bagging models capture with superior variance reduction and resilience against outliers.

---

## 🛠️ Data Pipeline & Feature Engineering

To guarantee zero data leakage between training and inference:
1. **Right-Skewed Transformation:** `Study_Hours` exhibits right-skewed distribution; stabilized using `np.log1p` followed by `StandardScaler`.
2. **Numeric Feature Scaling:** `Age`, `Avg_Daily_Usage_Hours`, `Daily_Unlocks`, `Physical_Activity_Hours`, and `Sleep_Hours_Per_Night` normalized via `StandardScaler`.
3. **Ordinal Encoding:** `Stress_Level` mapped ordinally (`Low` → `Medium` → `High` → `Very High`).
4. **Categorical Handling:** `Gender`, `Academic_Level`, `Most_Used_Platform`, `Purpose_Of_Use`, and `Grouped_country` (top 10 countries retained, sparse tails grouped into `'Other'`) transformed via `OneHotEncoder(handle_unknown='ignore')`.

```python
# Fully self-contained Scikit-Learn Preprocessing Pipeline
preprocessor = ColumnTransformer(transformers=[
    ('skewed', Pipeline([
        ('log', FunctionTransformer(np.log1p, feature_names_out='one-to-one')),
        ('scaler', StandardScaler())
    ]), ['Study_Hours']),
    ('numeric', StandardScaler(), [
        'Age', 'Avg_Daily_Usage_Hours', 'Daily_Unlocks',
        'Physical_Activity_Hours', 'Sleep_Hours_Per_Night'
    ]),
    ('ordinal', OrdinalEncoder(
        categories=[['Low', 'Medium', 'High', 'Very High']],
        handle_unknown='use_encoded_value',
        unknown_value=-1
    ), ['Stress_Level']),
    ('nominal', OneHotEncoder(handle_unknown='ignore'), [
        'Gender', 'Academic_Level', 'Most_Used_Platform', 'Purpose_Of_Use', 'Grouped_country'
    ])
])
```

---

## 💻 Tech Stack & Engineering Practices

| Domain | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend API** | FastAPI, Uvicorn, Pydantic v2 | High-performance asynchronous REST API serving serialized ML pipelines |
| **Frontend** | Streamlit, Custom Vanilla CSS | Interactive glassmorphic dashboard with live feedback & reactive state |
| **Machine Learning** | Scikit-Learn, XGBoost, Joblib | Model training, hyperparameter tuning, pipeline serialization |
| **Data & Analytics** | Pandas, NumPy, Matplotlib, Seaborn | Exploratory data analysis, statistical correlation profiling |
| **Deployment** | Streamlit Cloud, Uvicorn ASGI | Cloud hosting with automated continuous deployment from GitHub |

---

## 📂 Project Directory Structure

```plaintext
ML_mental_health_score/
├── backend/
│   ├── main.py              # FastAPI application, lifespan model loading, endpoints
│   └── schema.py            # Pydantic input/output schemas & type validators
├── frontend/
│   ├── app.py               # Streamlit multipage application entrypoint
│   ├── api_client.py        # Resilient HTTP client connecting frontend to backend
│   ├── components.py        # Reusable UI components (forms, score cards, recommendations)
│   └── styles.py            # Glassmorphic modern CSS styling & theme injection
├── models/
│   ├── train_and_save_models.py  # Model training, preprocessing pipeline, joblib persistence
│   ├── linear_regression.joblib  # Serialized Scikit-Learn Linear Regression pipeline
│   ├── random_forest.joblib      # Serialized Scikit-Learn Random Forest pipeline
│   ├── knn.joblib                # Serialized Scikit-Learn KNN pipeline
│   ├── svr.joblib                # Serialized Scikit-Learn SVR pipeline
│   └── xgboost.joblib            # Serialized XGBoost Regressor pipeline
├── Student Social Media And Mental Health Impact.csv  # 5,000-sample benchmark dataset
├── xgboost.ipynb            # Exploratory analysis & XGBoost experimentation
├── lr_and_rfr.ipynb         # Linear Regression & Random Forest notebook
├── svr.ipynb                # Support Vector Regressor experimentation
├── knn.ipynb                # K-Nearest Neighbors evaluation notebook
├── requirements.txt         # Production dependencies
└── README.md                # Project portfolio documentation
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Naren1122/ML_mental_health_score.git
cd ML_mental_health_score
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Retrain Models
```bash
python models/train_and_save_models.py
```

### 5. Launch the FastAPI Backend Service
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
* Interactive API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`
* API Alternative Docs (ReDoc): `http://127.0.0.1:8000/redoc`

### 6. Launch the Streamlit Frontend
In a separate terminal (with virtual environment active):
```bash
streamlit run frontend/app.py
```
Open `http://localhost:8501` in your browser.

---

## 📡 API Specification & Example Payloads

### `POST /predict` — Single Model Inference
**Request:**
```json
{
  "model_name": "random_forest",
  "features": {
    "Age": 21,
    "Gender": "Male",
    "Country": "USA",
    "Academic_Level": "Undergraduate",
    "Most_Used_Platform": "Instagram",
    "Purpose_Of_Use": "Entertainment",
    "Avg_Daily_Usage_Hours": 4.5,
    "Daily_Unlocks": 120,
    "Study_Hours": 4.0,
    "Physical_Activity_Hours": 1.5,
    "Sleep_Hours_Per_Night": 7.5,
    "Stress_Level": "Medium"
  }
}
```

**Response (HTTP 200 OK):**
```json
{
  "success": true,
  "prediction": {
    "model_key": "random_forest",
    "model_name": "Random Forest Regressor",
    "predicted_score": 6.84,
    "category": "Balanced & Healthy",
    "status_color": "#3B82F6",
    "recommendations": [
      "Well-balanced profile: Keep maintaining your daily equilibrium across study and rest."
    ]
  }
}
```

### `POST /predict/all` — Multi-Model Consensus
Runs simultaneous inference across all 5 models and returns an algorithmic consensus vector along with individualized scores.

---

## 👤 Author & Contact

**Narendra (Naren)**
* **Live App:** [MindScore on Streamlit](https://naren1122-ml-mental-health-score-frontendapp-unguti.streamlit.app/)
* **GitHub:** [@Naren1122](https://github.com/Naren1122)
* **Project Repository:** [Naren1122/ML_mental_health_score](https://github.com/Naren1122/ML_mental_health_score)

---
*Developed with focus on rigorous machine learning pipeline design, clean decoupled architecture, and human-centered health informatics.*
