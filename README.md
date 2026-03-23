# Smart Inventory AI Project

A machine learning-powered inventory management system that predicts demand and provides intelligent recommendations for stock levels and reordering.

## Features

- **Demand Forecasting**: Uses XGBoost model to predict future product demand based on historical data
- **Inventory Optimization**: Calculates optimal reorder points and quantities using EOQ (Economic Order Quantity)
- **Real-time Monitoring**: Web interface for checking inventory status and getting actionable insights
- **Multi-category Support**: Handles different product categories with varying demand patterns

## Project Overview

The Smart Inventory AI system revolutionizes retail inventory management by combining machine learning with traditional inventory optimization techniques. The system addresses common retail challenges like stockouts, overstocking, and inefficient ordering processes.

### How It Works

1. **Data Ingestion**: The system processes historical sales data, inventory levels, pricing information, and external factors like weather and seasonality.

2. **Demand Prediction**: Using an XGBoost machine learning model trained on time series data, the system forecasts future product demand for the next period.

3. **Inventory Analysis**: The system evaluates current inventory levels against calculated optimal thresholds:
   - **Reorder Point**: When stock falls below this level, new orders should be placed
   - **Safety Stock**: Buffer inventory to handle demand variability and supplier delays
   - **Economic Order Quantity (EOQ)**: Optimal order size that minimizes total inventory costs

4. **Decision Making**: Based on the analysis, the system provides actionable recommendations:
   - **UNDERSTOCK**: Immediate reordering required with suggested quantities
   - **OVERSTOCK**: Recommendations to stop ordering or apply promotions
   - **OK**: Inventory levels are optimal

5. **User Interface**: A simple web interface allows retail managers to check inventory status for any product category and receive instant recommendations.

### Business Value

- **Reduced Stockouts**: Accurate demand forecasting minimizes lost sales
- **Lower Holding Costs**: Optimal inventory levels reduce storage and carrying costs
- **Improved Cash Flow**: Better inventory turnover and reduced excess stock
- **Data-Driven Decisions**: Replaces manual guesswork with AI-powered insights
- **Scalable Solution**: Handles multiple product categories and store locations

### Technical Architecture

- **Backend**: FastAPI provides RESTful APIs for prediction and analysis
- **Frontend**: Streamlit offers an intuitive web interface
- **ML Model**: XGBoost regressor for demand forecasting
- **Data Processing**: Pandas and NumPy for efficient data manipulation
- **Business Logic**: Custom algorithms for inventory optimization calculations

## Project Structure

```
Smart-Inventory-Project/
├── backend/                 # FastAPI backend server
│   └── main.py             # Main API endpoints
├── frontend/               # Streamlit web interface
│   └── app.py              # User interface
├── data/                   # Dataset files
│   ├── retail_store_inventory.csv
│   └── sku_master.csv
├── models/                 # Trained ML models
│   └── model.pkl
├── notebooks/              # Jupyter notebooks for analysis
│   └── smart_inventory.ipynb
├── services/               # Business logic modules
│   ├── demand_forecasting.py
│   └── inventory_logic.py
└── requirements.txt        # Python dependencies
```

## Datasets

### retail_store_inventory.csv

Daily inventory and sales data containing:

- **Date**: Transaction date
- **Store ID**: Store identifier
- **Product ID**: Product identifier
- **Category**: Product category (Groceries, Toys, Dairy, Personal Care)
- **Region**: Geographic region (North, South, East, West)
- **Inventory Level**: Current stock quantity
- **Units Sold**: Daily sales volume
- **Units Ordered**: Replenishment orders
- **Demand Forecast**: Historical forecast values
- **Price**: Product price
- **Discount**: Applied discount percentage
- **Weather Condition**: Weather impact (Sunny, Rainy, Cloudy)
- **Holiday/Promotion**: Special event indicators
- **Competitor Pricing**: Market competitor prices
- **Seasonality**: Seasonal factors

### sku_master.csv

Product master data with business parameters:

- **SKU_ID**: Unique product identifier
- **Item_Name**: Product name
- **Category**: Product category
- **Shelf_Life_Days**: Product shelf life
- **Supplier_Lead_Time**: Days to receive new stock
- **Min_Order_Qty**: Minimum order quantity
- **Holding_Cost_Per_Unit**: Cost of holding inventory
- **Ordering_Cost**: Fixed cost per order

## Notebook: smart_inventory.ipynb

Jupyter notebook containing the complete data science workflow:

### Data Exploration

- Loading and initial inspection of datasets
- Statistical analysis and data quality checks
- Handling missing values and duplicates
- Feature engineering and preprocessing

### Exploratory Data Analysis (EDA)

- Sales trends and seasonality analysis
- Category-wise performance insights
- Regional demand patterns
- Correlation analysis between features

### Feature Engineering

- Time series features (lags, rolling averages)
- Categorical encoding
- Price and competitor analysis features
- Date-based features (day of week, month, season)

### Model Development

- XGBoost regression model for demand forecasting
- Feature selection and importance analysis
- Model training and validation
- Performance metrics evaluation

### Business Logic Implementation

- Economic Order Quantity (EOQ) calculations
- Reorder point determination
- Safety stock calculations
- Inventory status classification

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Start the Backend API**:

   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

2. **Start the Frontend Interface**:
   ```bash
   streamlit run frontend/app.py
   ```
   The web interface will be available at `http://localhost:8501`

### API Endpoints

- `GET /` - Health check
- `GET /predict/{category}` - Get inventory prediction for a product category

Example API response:

```json
{
  "SKU_ID": "Groceries",
  "Predicted_Demand": 47.91,
  "Inventory_Level": 117,
  "Status": "UNDERSTOCK",
  "Action": "Reorder 1271 units"
}
```

### Using the Web Interface

1. Open the Streamlit app in your browser
2. Enter a product category (e.g., "Groceries")
3. Click "Check Inventory Status"
4. View the predicted demand, current inventory, and recommended actions

## Model Details

- **Algorithm**: XGBoost Regressor
- **Target**: Units Sold (demand prediction)
- **Features**: 22 engineered features including temporal, categorical, and business metrics
- **Performance**: Trained on historical sales data with time series validation

## Business Logic

### Inventory Status Classification

- **UNDERSTOCK**: Current inventory < Reorder Point
- **OVERSTOCK**: Current inventory > 30 days of average demand
- **OK**: Inventory within optimal range

### Reorder Calculations

- **Reorder Point**: Lead Time Demand + Safety Stock
- **Safety Stock**: 1.2 × Average Daily Demand
- **EOQ**: Economic Order Quantity minimizing total inventory costs

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- Trained model file (`models/model.pkl`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and demonstration purposes.
