import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Smart Inventory AI", layout="centered")

st.title("🧠 Smart Inventory AI System")

sku_id = st.text_input("Enter Category name (eg. Grocery)")

if st.button("Check Inventory Status"):
    response = requests.get(f"{API_URL}/predict/{sku_id}")

    if response.status_code == 200:
        data = response.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.metric("Predicted Demand", data["Predicted_Demand"])
            st.metric("Inventory Level", data["Inventory_Level"])
            st.warning(f"Status: {data['Status']}")
            st.info(f"Suggested Action: {data['Action']}")
    else:
        st.error("Backend not reachable")
