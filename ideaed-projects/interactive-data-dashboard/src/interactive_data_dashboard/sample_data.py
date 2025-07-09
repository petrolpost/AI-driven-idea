"""Sample data generation module for Interactive Data Dashboard.

This module provides functions to generate various types of sample datasets
for demonstration, testing, and educational purposes.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from faker import Faker

# Configure logging
logger = logging.getLogger(__name__)
fake = Faker()


def generate_sales_data(n_records: int = 1000, 
                       start_date: str = '2023-01-01',
                       end_date: str = '2024-12-31') -> pd.DataFrame:
    """Generate sample sales data.
    
    Args:
        n_records: Number of records to generate
        start_date: Start date for the data
        end_date: End date for the data
        
    Returns:
        DataFrame with sales data
    """
    logger.info(f"Generating {n_records} sales records")
    
    np.random.seed(42)  # For reproducible results
    
    # Date range
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    dates = pd.date_range(start=start, end=end, freq='D')
    
    # Product categories and names
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys']
    products = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes'],
        'Home & Garden': ['Sofa', 'Table', 'Lamp', 'Plant', 'Curtains'],
        'Sports': ['Basketball', 'Tennis Racket', 'Running Shoes', 'Yoga Mat', 'Bicycle'],
        'Books': ['Fiction', 'Non-Fiction', 'Textbook', 'Comic', 'Biography'],
        'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'Building Blocks']
    }
    
    # Sales regions
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    # Generate data
    data = []
    for _ in range(n_records):
        category = np.random.choice(categories)
        product = np.random.choice(products[category])
        region = np.random.choice(regions)
        date = np.random.choice(dates)
        
        # Price varies by category
        price_ranges = {
            'Electronics': (100, 2000),
            'Clothing': (20, 200),
            'Home & Garden': (50, 1000),
            'Sports': (25, 500),
            'Books': (10, 50),
            'Toys': (15, 100)
        }
        
        min_price, max_price = price_ranges[category]
        unit_price = np.random.uniform(min_price, max_price)
        quantity = np.random.randint(1, 10)
        total_amount = unit_price * quantity
        
        # Add some seasonality
        month = date.month
        if category == 'Toys' and month in [11, 12]:  # Holiday boost for toys
            quantity = int(quantity * 1.5)
            total_amount = unit_price * quantity
        elif category == 'Clothing' and month in [3, 4, 9, 10]:  # Seasonal clothing
            quantity = int(quantity * 1.3)
            total_amount = unit_price * quantity
        
        # Customer information
        customer_id = f"CUST_{np.random.randint(1000, 9999)}"
        customer_age = np.random.randint(18, 80)
        customer_gender = np.random.choice(['Male', 'Female', 'Other'])
        
        data.append({
            'Date': date,
            'Customer_ID': customer_id,
            'Customer_Age': customer_age,
            'Customer_Gender': customer_gender,
            'Region': region,
            'Category': category,
            'Product': product,
            'Quantity': quantity,
            'Unit_Price': round(unit_price, 2),
            'Total_Amount': round(total_amount, 2),
            'Discount': round(np.random.uniform(0, 0.2), 2),
            'Sales_Rep': fake.name(),
            'Payment_Method': np.random.choice(['Credit Card', 'Cash', 'Debit Card', 'Online'])
        })
    
    df = pd.DataFrame(data)
    
    # Add derived columns
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Final_Amount'] = df['Total_Amount'] * (1 - df['Discount'])
    
    logger.info(f"Generated sales data with shape: {df.shape}")
    return df


def generate_employee_data(n_records: int = 500) -> pd.DataFrame:
    """Generate sample employee data.
    
    Args:
        n_records: Number of employee records to generate
        
    Returns:
        DataFrame with employee data
    """
    logger.info(f"Generating {n_records} employee records")
    
    np.random.seed(42)
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    positions = {
        'Engineering': ['Software Engineer', 'Senior Engineer', 'Tech Lead', 'Engineering Manager'],
        'Sales': ['Sales Rep', 'Account Manager', 'Sales Director', 'VP Sales'],
        'Marketing': ['Marketing Specialist', 'Marketing Manager', 'Brand Manager', 'CMO'],
        'HR': ['HR Specialist', 'HR Manager', 'Recruiter', 'CHRO'],
        'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager', 'CFO'],
        'Operations': ['Operations Specialist', 'Operations Manager', 'VP Operations']
    }
    
    locations = ['New York', 'San Francisco', 'Chicago', 'Austin', 'Seattle', 'Boston']
    
    data = []
    for i in range(n_records):
        department = np.random.choice(departments)
        position = np.random.choice(positions[department])
        location = np.random.choice(locations)
        
        # Salary ranges by position level
        salary_multipliers = {
            'Specialist': (50000, 80000),
            'Analyst': (55000, 85000),
            'Rep': (45000, 75000),
            'Engineer': (70000, 120000),
            'Manager': (90000, 150000),
            'Senior': (100000, 160000),
            'Director': (130000, 200000),
            'Lead': (110000, 170000),
            'VP': (150000, 250000),
            'C': (200000, 400000)  # C-level executives
        }
        
        # Determine salary range based on position
        salary_range = (60000, 100000)  # default
        for key, range_val in salary_multipliers.items():
            if key in position:
                salary_range = range_val
                break
        
        salary = np.random.randint(salary_range[0], salary_range[1])
        
        # Experience and age correlation
        years_experience = np.random.randint(0, 25)
        age = min(65, max(22, years_experience + np.random.randint(22, 30)))
        
        # Performance rating
        performance = np.random.choice(['Excellent', 'Good', 'Satisfactory', 'Needs Improvement'],
                                     p=[0.2, 0.4, 0.3, 0.1])
        
        # Hire date
        hire_date = fake.date_between(start_date='-10y', end_date='today')
        
        data.append({
            'Employee_ID': f"EMP_{i+1:04d}",
            'Name': fake.name(),
            'Age': age,
            'Gender': np.random.choice(['Male', 'Female', 'Other'], p=[0.45, 0.45, 0.1]),
            'Department': department,
            'Position': position,
            'Location': location,
            'Salary': salary,
            'Years_Experience': years_experience,
            'Hire_Date': hire_date,
            'Performance_Rating': performance,
            'Education_Level': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'],
                                              p=[0.1, 0.5, 0.3, 0.1]),
            'Remote_Work': np.random.choice(['Yes', 'No'], p=[0.4, 0.6]),
            'Bonus': np.random.randint(0, int(salary * 0.3)),
            'Training_Hours': np.random.randint(0, 100)
        })
    
    df = pd.DataFrame(data)
    
    # Add derived columns
    df['Hire_Date'] = pd.to_datetime(df['Hire_Date'])
    df['Years_at_Company'] = (datetime.now() - df['Hire_Date']).dt.days / 365.25
    df['Total_Compensation'] = df['Salary'] + df['Bonus']
    
    logger.info(f"Generated employee data with shape: {df.shape}")
    return df


def generate_financial_data(n_records: int = 1000,
                           start_date: str = '2020-01-01') -> pd.DataFrame:
    """Generate sample financial/stock data.
    
    Args:
        n_records: Number of records to generate
        start_date: Start date for the data
        
    Returns:
        DataFrame with financial data
    """
    logger.info(f"Generating {n_records} financial records")
    
    np.random.seed(42)
    
    # Stock symbols
    stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX']
    
    # Generate date range
    start = pd.to_datetime(start_date)
    dates = pd.date_range(start=start, periods=n_records//len(stocks), freq='D')
    
    data = []
    
    for stock in stocks:
        # Initial price
        initial_price = np.random.uniform(50, 300)
        price = initial_price
        
        for date in dates:
            # Random walk for price movement
            daily_return = np.random.normal(0.001, 0.02)  # Mean return with volatility
            price = price * (1 + daily_return)
            
            # Ensure price doesn't go negative
            price = max(price, 1)
            
            # Volume (higher volume on larger price movements)
            base_volume = np.random.randint(1000000, 10000000)
            volume_multiplier = 1 + abs(daily_return) * 5
            volume = int(base_volume * volume_multiplier)
            
            # OHLC data
            open_price = price * np.random.uniform(0.98, 1.02)
            high_price = max(open_price, price) * np.random.uniform(1.0, 1.05)
            low_price = min(open_price, price) * np.random.uniform(0.95, 1.0)
            close_price = price
            
            data.append({
                'Date': date,
                'Symbol': stock,
                'Open': round(open_price, 2),
                'High': round(high_price, 2),
                'Low': round(low_price, 2),
                'Close': round(close_price, 2),
                'Volume': volume,
                'Daily_Return': round(daily_return * 100, 2),
                'Market_Cap': round(price * np.random.randint(1000000, 10000000), 0)
            })
    
    df = pd.DataFrame(data)
    
    # Add technical indicators
    df = df.sort_values(['Symbol', 'Date'])
    
    for stock in stocks:
        stock_data = df[df['Symbol'] == stock].copy()
        
        # Moving averages
        stock_data['MA_7'] = stock_data['Close'].rolling(window=7).mean()
        stock_data['MA_30'] = stock_data['Close'].rolling(window=30).mean()
        
        # Volatility (rolling standard deviation)
        stock_data['Volatility'] = stock_data['Daily_Return'].rolling(window=30).std()
        
        # Update main dataframe
        df.loc[df['Symbol'] == stock, 'MA_7'] = stock_data['MA_7']
        df.loc[df['Symbol'] == stock, 'MA_30'] = stock_data['MA_30']
        df.loc[df['Symbol'] == stock, 'Volatility'] = stock_data['Volatility']
    
    # Add derived columns
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Day_of_Week'] = df['Date'].dt.day_name()
    
    logger.info(f"Generated financial data with shape: {df.shape}")
    return df


def generate_customer_data(n_records: int = 2000) -> pd.DataFrame:
    """Generate sample customer data.
    
    Args:
        n_records: Number of customer records to generate
        
    Returns:
        DataFrame with customer data
    """
    logger.info(f"Generating {n_records} customer records")
    
    np.random.seed(42)
    
    data = []
    
    for i in range(n_records):
        # Customer demographics
        age = np.random.randint(18, 80)
        gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.45, 0.45, 0.1])
        
        # Income correlated with age (peak earning years)
        if age < 25:
            income_range = (25000, 50000)
        elif age < 35:
            income_range = (40000, 80000)
        elif age < 50:
            income_range = (50000, 120000)
        elif age < 65:
            income_range = (45000, 100000)
        else:
            income_range = (30000, 70000)
        
        income = np.random.randint(income_range[0], income_range[1])
        
        # Customer behavior
        registration_date = fake.date_between(start_date='-3y', end_date='today')
        last_purchase = fake.date_between(start_date=registration_date, end_date='today')
        
        # Purchase behavior correlated with income
        total_spent = np.random.uniform(income * 0.05, income * 0.3)
        num_purchases = np.random.randint(1, 50)
        avg_order_value = total_spent / num_purchases if num_purchases > 0 else 0
        
        # Customer satisfaction
        satisfaction = np.random.choice(['Very Satisfied', 'Satisfied', 'Neutral', 
                                       'Dissatisfied', 'Very Dissatisfied'],
                                      p=[0.3, 0.4, 0.2, 0.08, 0.02])
        
        # Geographic data
        country = np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia'],
                                 p=[0.4, 0.15, 0.15, 0.1, 0.1, 0.1])
        
        if country == 'USA':
            state = np.random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'])
        else:
            state = None
        
        data.append({
            'Customer_ID': f"CUST_{i+1:06d}",
            'Name': fake.name(),
            'Email': fake.email(),
            'Age': age,
            'Gender': gender,
            'Country': country,
            'State': state,
            'City': fake.city(),
            'Income': income,
            'Registration_Date': registration_date,
            'Last_Purchase_Date': last_purchase,
            'Total_Spent': round(total_spent, 2),
            'Number_of_Purchases': num_purchases,
            'Average_Order_Value': round(avg_order_value, 2),
            'Customer_Satisfaction': satisfaction,
            'Preferred_Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books']),
            'Marketing_Channel': np.random.choice(['Email', 'Social Media', 'Search', 'Referral', 'Direct'],
                                                p=[0.25, 0.2, 0.2, 0.15, 0.2]),
            'Loyalty_Program': np.random.choice(['Yes', 'No'], p=[0.6, 0.4]),
            'Newsletter_Subscriber': np.random.choice(['Yes', 'No'], p=[0.7, 0.3])
        })
    
    df = pd.DataFrame(data)
    
    # Convert dates
    df['Registration_Date'] = pd.to_datetime(df['Registration_Date'])
    df['Last_Purchase_Date'] = pd.to_datetime(df['Last_Purchase_Date'])
    
    # Add derived columns
    df['Days_Since_Registration'] = (datetime.now() - df['Registration_Date']).dt.days
    df['Days_Since_Last_Purchase'] = (datetime.now() - df['Last_Purchase_Date']).dt.days
    df['Customer_Lifetime_Value'] = df['Total_Spent'] * np.random.uniform(1.2, 3.0, len(df))
    
    # Customer segments based on behavior
    def categorize_customer(row):
        if row['Total_Spent'] > 5000 and row['Number_of_Purchases'] > 20:
            return 'VIP'
        elif row['Total_Spent'] > 2000 and row['Number_of_Purchases'] > 10:
            return 'Loyal'
        elif row['Days_Since_Last_Purchase'] > 365:
            return 'Inactive'
        elif row['Number_of_Purchases'] <= 2:
            return 'New'
        else:
            return 'Regular'
    
    df['Customer_Segment'] = df.apply(categorize_customer, axis=1)
    
    logger.info(f"Generated customer data with shape: {df.shape}")
    return df


def generate_survey_data(n_records: int = 1500) -> pd.DataFrame:
    """Generate sample survey data.
    
    Args:
        n_records: Number of survey responses to generate
        
    Returns:
        DataFrame with survey data
    """
    logger.info(f"Generating {n_records} survey responses")
    
    np.random.seed(42)
    
    # Survey questions and response scales
    likert_scale = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    satisfaction_scale = ['Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied']
    frequency_scale = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
    
    data = []
    
    for i in range(n_records):
        # Respondent demographics
        age_group = np.random.choice(['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
                                   p=[0.15, 0.25, 0.25, 0.2, 0.1, 0.05])
        
        gender = np.random.choice(['Male', 'Female', 'Other', 'Prefer not to say'],
                                p=[0.45, 0.45, 0.05, 0.05])
        
        education = np.random.choice(['High School', 'Some College', 'Bachelor', 'Master', 'PhD'],
                                   p=[0.2, 0.2, 0.35, 0.2, 0.05])
        
        income_bracket = np.random.choice(['<$25k', '$25k-$50k', '$50k-$75k', 
                                         '$75k-$100k', '$100k-$150k', '>$150k'],
                                        p=[0.15, 0.25, 0.25, 0.2, 0.1, 0.05])
        
        # Survey responses (with some correlation)
        overall_satisfaction = np.random.choice(satisfaction_scale, p=[0.05, 0.1, 0.2, 0.45, 0.2])
        
        # Product quality tends to correlate with overall satisfaction
        if overall_satisfaction in ['Very Satisfied', 'Satisfied']:
            product_quality = np.random.choice(likert_scale, p=[0.02, 0.08, 0.15, 0.45, 0.3])
        else:
            product_quality = np.random.choice(likert_scale, p=[0.2, 0.3, 0.3, 0.15, 0.05])
        
        # Customer service rating
        customer_service = np.random.choice(satisfaction_scale, p=[0.08, 0.12, 0.25, 0.35, 0.2])
        
        # Usage frequency
        usage_frequency = np.random.choice(frequency_scale, p=[0.1, 0.15, 0.3, 0.3, 0.15])
        
        # Recommendation likelihood (NPS-style)
        nps_score = np.random.randint(0, 11)
        
        # Brand perception
        brand_trust = np.random.choice(likert_scale, p=[0.05, 0.1, 0.2, 0.4, 0.25])
        value_for_money = np.random.choice(likert_scale, p=[0.08, 0.15, 0.25, 0.35, 0.17])
        
        # Purchase intent
        purchase_intent = np.random.choice(['Definitely will not', 'Probably will not', 
                                          'Might or might not', 'Probably will', 'Definitely will'],
                                         p=[0.1, 0.15, 0.3, 0.3, 0.15])
        
        data.append({
            'Response_ID': f"RESP_{i+1:06d}",
            'Survey_Date': fake.date_between(start_date='-6m', end_date='today'),
            'Age_Group': age_group,
            'Gender': gender,
            'Education': education,
            'Income_Bracket': income_bracket,
            'Overall_Satisfaction': overall_satisfaction,
            'Product_Quality': product_quality,
            'Customer_Service': customer_service,
            'Usage_Frequency': usage_frequency,
            'NPS_Score': nps_score,
            'Brand_Trust': brand_trust,
            'Value_for_Money': value_for_money,
            'Purchase_Intent': purchase_intent,
            'Survey_Channel': np.random.choice(['Email', 'Website', 'Phone', 'In-store'],
                                             p=[0.4, 0.3, 0.2, 0.1]),
            'Response_Time_Minutes': np.random.randint(2, 30),
            'Complete_Response': np.random.choice(['Yes', 'No'], p=[0.85, 0.15])
        })
    
    df = pd.DataFrame(data)
    
    # Convert survey date
    df['Survey_Date'] = pd.to_datetime(df['Survey_Date'])
    
    # Add derived columns
    df['Month'] = df['Survey_Date'].dt.month
    df['Quarter'] = df['Survey_Date'].dt.quarter
    
    # NPS categorization
    def nps_category(score):
        if score >= 9:
            return 'Promoter'
        elif score >= 7:
            return 'Passive'
        else:
            return 'Detractor'
    
    df['NPS_Category'] = df['NPS_Score'].apply(nps_category)
    
    # Satisfaction score (numeric)
    satisfaction_mapping = {
        'Very Dissatisfied': 1,
        'Dissatisfied': 2,
        'Neutral': 3,
        'Satisfied': 4,
        'Very Satisfied': 5
    }
    
    df['Satisfaction_Score'] = df['Overall_Satisfaction'].map(satisfaction_mapping)
    
    logger.info(f"Generated survey data with shape: {df.shape}")
    return df


def get_sample_datasets() -> Dict[str, callable]:
    """Get dictionary of available sample dataset generators.
    
    Returns:
        Dictionary mapping dataset names to generator functions
    """
    return {
        'Sales Data': generate_sales_data,
        'Employee Data': generate_employee_data,
        'Financial Data': generate_financial_data,
        'Customer Data': generate_customer_data,
        'Survey Data': generate_survey_data
    }


def generate_custom_dataset(dataset_type: str, **kwargs) -> pd.DataFrame:
    """Generate a custom dataset based on type and parameters.
    
    Args:
        dataset_type: Type of dataset to generate
        **kwargs: Additional parameters for the generator
        
    Returns:
        Generated DataFrame
    """
    generators = get_sample_datasets()
    
    if dataset_type not in generators:
        raise ValueError(f"Unknown dataset type: {dataset_type}. Available types: {list(generators.keys())}")
    
    generator = generators[dataset_type]
    return generator(**kwargs)


def get_dataset_info() -> Dict[str, Dict[str, str]]:
    """Get information about available sample datasets.
    
    Returns:
        Dictionary with dataset information
    """
    return {
        'Sales Data': {
            'description': 'E-commerce sales transactions with customer demographics, product categories, and regional data',
            'columns': 'Date, Customer info, Product details, Sales metrics, Regional data',
            'use_cases': 'Sales analysis, trend analysis, customer segmentation, regional performance'
        },
        'Employee Data': {
            'description': 'HR dataset with employee information, salaries, performance, and organizational data',
            'columns': 'Employee details, Department, Position, Salary, Performance, Experience',
            'use_cases': 'HR analytics, compensation analysis, performance evaluation, diversity metrics'
        },
        'Financial Data': {
            'description': 'Stock market data with OHLC prices, volume, and technical indicators',
            'columns': 'Date, Symbol, OHLC prices, Volume, Returns, Technical indicators',
            'use_cases': 'Financial analysis, portfolio management, technical analysis, market trends'
        },
        'Customer Data': {
            'description': 'Customer profiles with demographics, purchase behavior, and engagement metrics',
            'columns': 'Customer details, Demographics, Purchase history, Satisfaction, Segmentation',
            'use_cases': 'Customer analytics, segmentation, lifetime value analysis, churn prediction'
        },
        'Survey Data': {
            'description': 'Survey responses with satisfaction ratings, NPS scores, and demographic breakdowns',
            'columns': 'Response details, Demographics, Satisfaction ratings, NPS, Brand perception',
            'use_cases': 'Customer satisfaction analysis, NPS tracking, market research, brand analysis'
        }
    }