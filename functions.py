import pandas as pd
from datetime import datetime

# Sample items
items = [
    {"price": 4300, "category": "Food", "date": "12-6-2024", "item": "Large Eggs"},
    {"price": 1500, "category": "Transportation", "date": "12-5-2024", "item": "Bus tickets"},
    {
        "price": 2000,
        "category": "Housing",
        "date": "12-5-2024",
        "item": "Double A Batteries",
    },
    {
        "price": 2500,
        "category": "Shopping",
        "date": "12-3-2024",
        "item": "Toilet paper roll",
    },
    {
        "price": 5000,
        "category": "Housing",
        "date": "12-2-2024",
        "item": "Extension cord",
    },
    {"price": 750, "category": "Shopping", "date": "12-4-2024", "item": "Paper plates"},
    {"price": 3000, "category": "Entertainment", "date": "12-1-2024", "item": "JB Concert"},
    {"price": 4300, "category": "Food", "date": "11-6-2024", "item": "Milk"},
    {"price": 1500, "category": "Transportation", "date": "11-5-2024", "item": "Train season"},
    {"price": 2000, "category": "Housing", "date": "11-5-2024", "item": "Hot plate"},
    {"price": 2500, "category": "Shopping", "date": "10-3-2024", "item": "Sarongs"},
    {"price": 5000, "category": "Housing", "date": "1-2-2024", "item": "Multiplug mega"},
    {"price": 750, "category": "Shopping", "date": "1-4-2024", "item": "Hat"},
    {"price": 3000, "category": "Entertainment", "date": "2-1-2024", "item": "Pool day"},
    {"price": 4300, "category": "Food", "date": "12-6-2023", "item": "Yogurt"},
    {"price": 1500, "category": "Transportation", "date": "12-5-2023", "item": "Train ticket"},
    {"price": 2000, "category": "Housing", "date": "12-5-2023", "item": "Water bill"},
    {"price": 2500, "category": "Shopping", "date": "12-3-2023", "item": "Sneakers"},
    {"price": 5000, "category": "Housing", "date": "12-2-2023", "item": "Dialog charges"},
    {"price": 750, "category": "Shopping", "date": "12-4-2023", "item": "Ladies Blouse"},
    {"price": 3000, "category": "Entertainment", "date": "12-1-2023", "item": "Interstellar movie"},
    {"price": 4300, "category": "Food", "date": "11-6-2023", "item": "Cottage Cheese"},
    {"price": 1500, "category": "Transportation", "date": "11-5-2023", "item": "Van hire"},
    {"price": 2000, "category": "Housing", "date": "11-5-2023", "item": "Thinner can"},
    {"price": 2500, "category": "Shopping", "date": "10-3-2023", "item": "Bulb kit"},
    {"price": 5000, "category": "Housing", "date": "1-2-2023", "item": "SLT Broadband"},
    {"price": 750, "category": "Shopping", "date": "1-4-2023", "item": "Seat cover"},
    {"price": 25, "category": "Healthcare", "date": "10-3-2023", "item": "Panadol"},
    {"price": 5000, "category": "Other", "date": "1-2-2023", "item": "Laptop repair"},
    {"price": 750, "category": "Healthcare", "date": "1-4-2023", "item": "Gel Oinment"},
    {"price": 3000, "category": "Other", "date": "2-1-2023", "item": "Donation to childrens' care"},
    {"price": 3000, "category": "Entertainment", "date": "2-1-2023", "item": "BnS Concert"},
]


# Load data
def load_data():
    df = pd.DataFrame(items)
    df["date"] = pd.to_datetime(df["date"], format="%m-%d-%Y")
    df = df.sort_values(by="date")
    df["cumulative_sum"] = df.groupby("category")["price"].cumsum()

    unique_categories = df["category"].unique()
    category_totals = df.groupby("category")["price"].sum().to_dict()
    thresholds = {category: float("inf") for category in unique_categories}

    return df, category_totals, thresholds


# Spending description
# def spending_description(total, threshold):
#     return "Within limit" if total <= threshold else "Threshold exceeded"


# Display category items
def display_category_items(category):
    return [item for item in items if item["category"] == category]


# Save settings
def update_settings(start_date, max_threshold, thresholds):
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "max_threshold": max_threshold,
        "thresholds": thresholds,
    }
