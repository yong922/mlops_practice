import mlflow
import pandas as pd
from fastapi import FastAPI
from schemas import PredictIn, PredictOut
from preprocessing import preprocess_input


def get_model():
    model = mlflow.sklearn.load_model(model_uri="./lgbm_model")
    return model

MODEL = get_model()


app = FastAPI()

@app.post("/predict", response_model=PredictOut)
def predict(data: PredictIn) -> PredictOut:
    df = pd.DataFrame([data.dict()])
    df = preprocess_input(df)
    pred = MODEL.predict(df).item()
    return PredictOut(loan_grade=pred)