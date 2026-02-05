import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join("models", "model.pkl")
model = joblib.load(MODEL_PATH)

FEATURES = [
    'Inventory Level',
    'Price',
    'Discount',
    'Holiday/Promotion',
    'Competitor Pricing',
    'year',
    'month',
    'day',
    'day_of_week',
    'week_of_year',
    'is_weekend',
    'lag_7',
    'lag_14',
    'lag_30',
    'rolling_7',
    'rolling_14',
    'price_diff_comp',
    'discount_flag'
]

def predict_demand(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['predicted_demand'] = model.predict(df[FEATURES])
    return df
