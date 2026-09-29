from typing import Literal, List, Dict, Any
from pydantic import BaseModel, Field

GenderType = Literal['Female', 'Male']
AcademicLevelType = Literal['Graduate', 'High School', 'Undergraduate']
PlatformType = Literal[
    'Facebook', 'Instagram', 'KakaoTalk', 'LINE', 'LinkedIn',
    'Snapchat', 'TikTok', 'Twitter', 'VKontakte', 'WeChat', 'WhatsApp', 'YouTube'
]
PurposeType = Literal['Education', 'Entertainment', 'Networking', 'News']
StressLevelType = Literal['Low', 'Medium', 'High', 'Very High']

ModelNameType = Literal[
    'linear_regression', 'random_forest', 'knn', 'svr', 'xgboost'
]

class StudentFeatures(BaseModel):
    Age: int = Field(21, ge=16, le=40, description="Student age")
    Gender: GenderType = Field('Male')
    Country: str = Field('USA', description="Country of residence")
    Academic_Level: AcademicLevelType = Field('Undergraduate')
    Most_Used_Platform: PlatformType = Field('Instagram')
    Purpose_Of_Use: PurposeType = Field('Entertainment')
    Avg_Daily_Usage_Hours: float = Field(4.0, ge=0.0, le=24.0, description="Screen time in hours")
    Daily_Unlocks: int = Field(120, ge=0, le=600, description="Smartphone daily unlock count")
    Study_Hours: float = Field(3.5, ge=0.0, le=24.0, description="Daily study hours")
    Physical_Activity_Hours: float = Field(1.5, ge=0.0, le=12.0, description="Physical activity in hours")
    Sleep_Hours_Per_Night: float = Field(7.0, ge=0.0, le=16.0, description="Sleep hours per night")
    Stress_Level: StressLevelType = Field('Medium')

# 2. Prediction Request for a single model
class PredictionRequest(BaseModel):
    model_name: ModelNameType = Field('xgboost', description="Model to use")
    features: StudentFeatures

# 3. Output Response Schema
class ModelPrediction(BaseModel):
    model_key: str
    model_name: str
    predicted_score: float
    category: str
    status_color: str
    recommendations: List[str]

class PredictionResponse(BaseModel):
    success: bool
    prediction: ModelPrediction

# 4. Output Response Schema when comparing ALL models
class AllModelsPredictionResponse(BaseModel):
    success: bool
    predictions: Dict[str, float]
    category: str
    recommendations: List[str]
