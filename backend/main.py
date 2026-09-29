import os
from contextlib import asynccontextmanager
from typing import Dict, Any, List

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schema import (
    StudentFeatures,
    PredictionRequest,
    PredictionResponse,
    AllModelsPredictionResponse,
    ModelPrediction
)

# Locate the models directory
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))

# In-memory dictionary to hold loaded models
loaded_models: Dict[str, Any] = {}

MODEL_DISPLAY_NAMES = {
    'linear_regression': 'Linear Regression',
    'random_forest': 'Random Forest Regressor',
    'knn': 'K-Nearest Neighbors (KNN)',
    'svr': 'Support Vector Regressor (SVR)',
    'xgboost': 'XGBoost Regressor'
}

TOP_COUNTRIES = [
    'Other', 'India', 'USA', 'Canada', 'Australia', 
    'UK', 'Germany', 'Mexico', 'Turkey', 'France'
]

def get_mental_health_category(score: float):
    if score >= 8.0:
        return "Resilient & Thriving", "#10B981"         # Green
    elif score >= 6.5:
        return "Balanced & Healthy", "#3B82F6"          # Blue
    elif score >= 5.0:
        return "Mild Distress / Elevated Stress", "#F59E0B" # Amber
    else:
        return "High Distress / Needs Attention", "#EF4444" # Red

def generate_recommendations(features: StudentFeatures) -> List[str]:
    recs = []
    if features.Sleep_Hours_Per_Night < 6.0:
        recs.append(" Sleep Hygiene: Less than 6 hours sleep is strongly tied to emotional exhaustion. Aim for 7-8 hours.")
    elif features.Sleep_Hours_Per_Night >= 8.0:
        recs.append(" Great sleep consistency: Consistent circadian rhythm protects cognitive resilience.")

    if features.Avg_Daily_Usage_Hours >= 6.0:
        recs.append(" Digital Detox: Social media usage above 6 hours correlates with high anxiety and doomscrolling.")
    elif features.Avg_Daily_Usage_Hours <= 2.5:
        recs.append(" Mindful screen time: Your screen time is in a healthy psychological window.")

    if features.Daily_Unlocks >= 180:
        recs.append(" Notification Management: 180+ daily phone unlocks suggests frequent attention fragmentation.")

    if features.Physical_Activity_Hours < 1.0:
        recs.append(" Movement: Adding 30 minutes of aerobic activity or walking significantly boosts endorphins.")

    if features.Stress_Level in ['High', 'Very High']:
        recs.append(" Stress Relief: Consider scheduled breaks, mindfulness, or discussing workload with an advisor.")

    if not recs:
        recs.append(" Well-balanced profile: Keep maintaining your daily equilibrium across study and rest.")

    return recs

# Lifespan: Loads models once on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    global loaded_models
    for key in MODEL_DISPLAY_NAMES.keys():
        path = os.path.join(MODELS_DIR, f"{key}.joblib")
        if os.path.exists(path):
            loaded_models[key] = joblib.load(path)
            print(f" Loaded model: {key}")
        else:
            print(f" Warning: Model {path} not found.")
    yield
    loaded_models.clear()

app = FastAPI(
    title="Student Mental Health Score API",
    description="Backend API serving 5 ML models to evaluate student mental health.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS so Streamlit can communicate freely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def format_features_df(features: StudentFeatures) -> pd.DataFrame:
    # Match the 'Grouped_country' feature from training
    grouped_country = features.Country if features.Country in TOP_COUNTRIES else 'Other'
    
    return pd.DataFrame([{
        'Study_Hours': float(features.Study_Hours),
        'Age': int(features.Age),
        'Avg_Daily_Usage_Hours': float(features.Avg_Daily_Usage_Hours),
        'Daily_Unlocks': int(features.Daily_Unlocks),
        'Physical_Activity_Hours': float(features.Physical_Activity_Hours),
        'Sleep_Hours_Per_Night': float(features.Sleep_Hours_Per_Night),
        'Stress_Level': str(features.Stress_Level),
        'Gender': str(features.Gender),
        'Academic_Level': str(features.Academic_Level),
        'Most_Used_Platform': str(features.Most_Used_Platform),
        'Purpose_Of_Use': str(features.Purpose_Of_Use),
        'Grouped_country': str(grouped_country)
    }])

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "loaded_models": list(loaded_models.keys())
    }

@app.get("/models")
def get_models():
    return {"available_models": MODEL_DISPLAY_NAMES}

@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    model_key = payload.model_name
    if model_key not in loaded_models:
        raise HTTPException(status_code=400, detail=f"Model '{model_key}' is not available.")

    pipeline = loaded_models[model_key]
    df_input = format_features_df(payload.features)

    # Predict and clamp between 1.0 and 10.0
    raw_pred = float(pipeline.predict(df_input)[0])
    score = round(float(np.clip(raw_pred, 1.0, 10.0)), 2)

    category, color = get_mental_health_category(score)
    recommendations = generate_recommendations(payload.features)

    return PredictionResponse(
        success=True,
        prediction=ModelPrediction(
            model_key=model_key,
            model_name=MODEL_DISPLAY_NAMES[model_key],
            predicted_score=score,
            category=category,
            status_color=color,
            recommendations=recommendations
        )
    )

@app.post("/predict/all", response_model=AllModelsPredictionResponse)
def predict_all(features: StudentFeatures):
    if not loaded_models:
        raise HTTPException(status_code=503, detail="No models loaded.")

    df_input = format_features_df(features)
    predictions = {}

    for key, pipeline in loaded_models.items():
        score = float(np.clip(pipeline.predict(df_input)[0], 1.0, 10.0))
        predictions[key] = round(score, 2)

    avg_score = round(float(np.mean(list(predictions.values()))), 2)
    category, _ = get_mental_health_category(avg_score)
    recommendations = generate_recommendations(features)

    return AllModelsPredictionResponse(
        success=True,
        predictions=predictions,
        category=category,
        recommendations=recommendations
    )
