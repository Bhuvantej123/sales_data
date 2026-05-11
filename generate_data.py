import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data(num_rows=1000):
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Headphones', 'Cameras'],
        'Furniture': ['Chairs', 'Tables', 'Sofas', 'Beds'],
        'Office Supplies': ['Paper', 'Pens', 'Binders', 'Envelopes'],
        'Apparel': ['T-shirts', 'Jeans', 'Jackets', 'Shoes']
    }
    
    start_date = datetime(2023, 1, 1)
    
    data = []
    for _ in range(num_rows):
        order_date = start_date + timedelta(days=random.randint(0, 365*2))
        region = random.choice(regions)
        category = random.choice(list(categories.keys()))
        sub_category = random.choice(categories[category])
        
        # Sales and Profit logic
        sales = round(random.uniform(10, 5000), 2)
        quantity = random.randint(1, 10)
        # Higher profit for Electronics, lower for Furniture
        profit_margin = random.uniform(0.05, 0.4) if category != 'Furniture' else random.uniform(-0.1, 0.2)
        profit = round(sales * profit_margin, 2)
        discount = random.choice([0, 0.1, 0.2, 0.3])
        
        data.append([
            order_date.strftime('%Y-%m-%d'),
            region,
            category,
            sub_category,
            sales,
            quantity,
            profit,
            discount
        ])
        
    df = pd.DataFrame(data, columns=[
        'Order Date', 'Region', 'Category', 'Sub-Category', 'Sales', 'Quantity', 'Profit', 'Discount'
    ])
    
    # Sort by date
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df = df.sort_values('Order Date')
    
    df.to_csv('sales_data.csv', index=False)
    print(f"Generated {num_rows} rows of sales data in 'sales_data.csv'")

if __name__ == "__main__":
    generate_sales_data()
