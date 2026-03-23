
from fastapi import FastAPI
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

from services.demand_forecasting import predict_demand
from services.inventory_logic import inventory_decision

app = FastAPI(title="Smart Inventory AI Backend")

DATA_PATH = os.path.join("data", "retail_store_inventory.csv")
SKU_PATH = os.path.join("data", "sku_master.csv")

df = pd.read_csv(DATA_PATH)
df['Date'] = pd.to_datetime(df['Date'])

sku_master = pd.read_csv(SKU_PATH)

@app.get("/")
def root():
    return {"status": "Smart Inventory AI Backend Running"}

@app.get("/predict/{sku_id}")
def predict_sku(sku_id: str):

    sku_df = df[df['Category'] == sku_id].copy()

    if sku_df.empty:
        return {"error": "SKU not found"}

    # ---------- FEATURE ENGINEERING ----------
    sku_df = sku_df.sort_values("Date")

    sku_df['year'] = sku_df['Date'].dt.year
    sku_df['month'] = sku_df['Date'].dt.month
    sku_df['day'] = sku_df['Date'].dt.day
    sku_df['day_of_week'] = sku_df['Date'].dt.dayofweek
    sku_df['week_of_year'] = sku_df['Date'].dt.isocalendar().week.astype(int)
    sku_df['is_weekend'] = sku_df['day_of_week'].isin([5,6]).astype(int)

    sku_df['lag_7']  = sku_df['Units Sold'].shift(7)
    sku_df['lag_14'] = sku_df['Units Sold'].shift(14)
    sku_df['lag_30'] = sku_df['Units Sold'].shift(30)

    sku_df['rolling_7']  = sku_df['Units Sold'].shift(1).rolling(7).mean()
    sku_df['rolling_14'] = sku_df['Units Sold'].shift(1).rolling(14).mean()

    sku_df['price_diff_competitor'] = sku_df['Price'] - sku_df['Competitor Pricing']
    sku_df['discount_flag'] = (sku_df['Discount'] > 0).astype(int)

    sku_df = sku_df.dropna()

    # Encode categorical features
    sku_df['Category'] = sku_df['Category'].astype('category')
    sku_df['Region'] = sku_df['Region'].astype('category')
    sku_df['Weather Condition'] = sku_df['Weather Condition'].astype('category')
    sku_df['Seasonality'] = sku_df['Seasonality'].astype('category')

    sku_df = predict_demand(sku_df)
    latest = sku_df.iloc[-1]

    sku_info = sku_master[sku_master['Category'] == sku_id].iloc[0]

    combined = {k: float(v) if isinstance(v, (int, float)) else v for k, v in latest.to_dict().items()}
    combined.update({k: float(v) if isinstance(v, (int, float)) else v for k, v in sku_info.to_dict().items()})

    status, action = inventory_decision(combined)


    return {
        "SKU_ID": sku_id,
        "Predicted_Demand": round(latest['predicted_demand'].item(), 2),
        "Inventory_Level": int(latest['Inventory Level']),
        "Status": status,
        "Action": action
    }
