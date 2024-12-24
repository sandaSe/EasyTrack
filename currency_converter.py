import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your API key
api_key = os.getenv("ExchangeRate_API_KEY")


# Function to get conversion rate and perform the conversion
def convert_currency(base_currency, target_currency, amount, date=None):
    # If a date is provided, use the historical endpoint
    if date:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/history/{base_currency}/{date}"
    else:
        # If no date is provided, use the latest rates
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"

    # Send GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the response JSON

        if target_currency in data["conversion_rates"]:
            exchange_rate = data["conversion_rates"][target_currency]
            converted_amount = amount * exchange_rate
            return converted_amount
        else:
            raise ValueError(f"Error: Target currency {target_currency} not found.")
    else:
        raise ValueError("Error fetching exchange rates: " + str(response.status_code))
