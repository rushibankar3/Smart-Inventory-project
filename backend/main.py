from fastapi import FastAPI
import pandas as pd
import os

from services.demand_forecasting import predict_demand
from services.inventory_logic import inventory_decision

app = FastAPI(title="Smart Inventory AI Backend")

# Load data
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
    sku_df = df[df['SKU_ID'] == sku_id].copy()

    if len(sku_df) == 0:
        return {"error": "SKU not found"}

    sku_df = predict_demand(sku_df)

    latest = sku_df.iloc[-1]
    sku_info = sku_master[sku_master['SKU_ID'] == sku_id].iloc[0]

    combined = latest.to_dict()
    combined.update(sku_info.to_dict())

    status, action = inventory_decision(combined)

    return {
        "SKU_ID": sku_id,
        "Predicted_Demand": round(latest['predicted_demand'], 2),
        "Inventory_Level": int(latest['Inventory Level']),
        "Status": status,
        "Action": action
    }
