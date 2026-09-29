import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

def predict_single_model(model_name: str, features: dict):
    """Sends user features to FastAPI for a single model prediction."""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"model_name": model_name, "features": features}
        )
        if response.status_code == 200:
            return response.json()["prediction"]
        else:
            st.error(f"Backend Error ({response.status_code}): {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Could not connect to FastAPI! Ensure `python -m uvicorn backend.main:app --reload --port 8000` is running.")
        return None

def predict_all_models(features: dict):
    """Sends user features to FastAPI to get predictions from all 5 models."""
    try:
        response = requests.post(f"{API_URL}/predict/all", json=features)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend Error ({response.status_code}): {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Could not connect to FastAPI! Ensure your FastAPI server is running.")
        return None
