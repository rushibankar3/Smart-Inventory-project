import numpy as np

def inventory_decision(row):
    avg_daily_demand = max(1, row['rolling_7'] / 7)

    safety_stock = avg_daily_demand * 1.2
    rop = (avg_daily_demand * row['Supplier_Lead_Time']) + safety_stock

    eoq = np.sqrt(
        (2 * avg_daily_demand * 365 * row['Ordering_Cost']) /
        row['Holding_Cost_Per_Unit']
    )

    eoq = max(int(eoq), row['Min_Order_Qty'])

    if row['Inventory Level'] < rop:
        return "UNDERSTOCK", f"Reorder {eoq} units"

    if row['Inventory Level'] > avg_daily_demand * 30:
        return "OVERSTOCK", "Stop ordering / apply discount"

    return "OK", "No action required"
