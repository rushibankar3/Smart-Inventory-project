import joblib
import pandas as pd
import os
import xgboost as xgb

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
    'price_diff_competitor',
    'discount_flag',
    'Category',
    'Region',
    'Weather Condition',
    'Seasonality'
]

def predict_demand(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    dmatrix = xgb.DMatrix(df[FEATURES], enable_categorical=True)
    df['predicted_demand'] = model.get_booster().predict(dmatrix)
    return df
