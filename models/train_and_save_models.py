import os
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer


from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor


df = pd.read_csv('Student Social Media And Mental Health Impact.csv')
df = df.drop_duplicates().copy()
df['Physical_Activity_Hours'] = df['Physical_Activity_Hours'].clip(lower=0)


top_countries = df['Country'].value_counts().index[:10].tolist()
df['Grouped_country'] = df['Country'].where(df['Country'].isin(top_countries), other='Other')


skewed_col = ['Study_Hours']
numeric_cols = [
    'Age', 'Avg_Daily_Usage_Hours', 'Daily_Unlocks',
    'Physical_Activity_Hours', 'Sleep_Hours_Per_Night'
]
ordinal_col = ['Stress_Level']
nominal_col = ['Gender', 'Academic_Level', 'Most_Used_Platform', 'Purpose_Of_Use', 'Grouped_country']
feature_cols = skewed_col + numeric_cols + ordinal_col + nominal_col
X = df[feature_cols]
y = df['Mental_Health_Score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)


def get_preprocessor():
    return ColumnTransformer(transformers=[
        ('skewed', Pipeline([
            ('log', FunctionTransformer(np.log1p, feature_names_out='one-to-one')),
            ('scaler', StandardScaler())
        ]), skewed_col),
        ('numeric', StandardScaler(), numeric_cols),
        ('ordinal', OrdinalEncoder(
            categories=[['Low', 'Medium', 'High', 'Very High']],
            handle_unknown='use_encoded_value',
            unknown_value=-1
        ), ordinal_col),
        ('nominal', OneHotEncoder(handle_unknown='ignore'), nominal_col)
    ])


models = {
    'linear_regression': LinearRegression(),
    'random_forest': RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
    'knn': KNeighborsRegressor(n_neighbors=5),
    'svr': SVR(kernel='rbf', C=1.0, epsilon=0.1),
    'xgboost': XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4, random_state=42, n_jobs=-1)
}


os.makedirs('models', exist_ok=True)
for model_key, estimator in models.items():
    pipeline = Pipeline(steps=[
        ('preprocessor', get_preprocessor()),
        ('model', estimator)
    ])
    pipeline.fit(X_train, y_train)
    
    file_path = os.path.join('models', f'{model_key}.joblib')
    joblib.dump(pipeline, file_path)
    print(f" Saved: {file_path}")
print("All 5 models are saved in the models/ folder!")
