import google.generativeai as genai
import re


def process_bill_data(input_variables, api_key):
    # Configure the API key
    genai.configure(api_key=api_key)

    # Set generation configuration
    generation_config = {
        "temperature": 0,
        "top_p": 0.05,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", generation_config=generation_config
    )

    # Create the system prompt using input variables
    system_prompt = f"""You are a smart text analysis assistant designed to process extracted text from scanned bills.

    You will receive:
    - A block of text extracted from a scanned bill: {input_variables['extracted_data_from_bill']}.
    - Additional contextual details: {input_variables['entities']}.

    Your tasks are as follows:

    1. Classify Bills:
       Identify the type of bill based on its structure and content.
          Type 1: Multi-line bills (e.g., grocery bills, restaurant bills, household item bills, clothing store bills, medical bills with multiple entries).
          Type 2: Single-item bills (e.g., utility bills under housing (electricity/water/internet), tickets under transportation (railway/air/bus), concert or movie tickets under entertainment).

    2. Extract and Categorize Items:
       a) Identify and categorize items:
          - Analyze the extracted text to identify individual items, their prices, and any additional details (e.g., bill name).
          - Assign each item to a predefined category:
              - Food: Groceries, restaurants, coffee, snacks
              - Transportation: Gas, public transport (bus/train/air), car payments, parking tolls
              - Housing: Rent/mortgage, utilities (electricity, water, gas, internet), home repairs/enhancements
              - Shopping: Clothing, electronics, household items, personal care
              - Entertainment: Movies, concerts, hobbies, gym, subscriptions, community events
              - Healthcare: Medicine, doctor visits, medical tests
              - Other: Items that don't fit into the above categories

       b) Identify the date, currency and total amount:
          - Extract the date, currency and total amount from the text.
              - If multiple amounts are identified as totals, select the highest value as bill total. This is different from the individual prices of items.
              - Use contextual information (e.g., addresses/locations/telephone numbers) to infer the relevant currency. Give the currency in standard format (LKR, EUR, etc.).
                (example: Rs. means LKR for Sri Lankan bills)
              - If no valid date is found in {input_variables['extracted_data_from_bill']} or {input_variables['entities']}, use {input_variables['date']}.

    3. Summarize Results:
       Output a clear breakdown of items, their prices, categories, and the total bill amount in a structured JSON format.
       Make sure the JSON structure is valid and properly formatted.

    Constraints and Assumptions:
      - Some items may have ambiguous names. Use context from surrounding entries or common usage patterns to determine their categories.
      - Handle variations in formatting, spelling, or currency representation.

    Output Format Examples:

    Type 1 Bill (Multi-line):
        ```
          [
              {{"date": "12-6-2024", "category": "Food", "item": "Large Eggs", "price": 630, "total": 8680, "currency": "LKR"}},
              {{"date": "12-6-2024", "category": "Food", "item": "Pizza toppings", "price": 1500, "total": 8680, "currency": "LKR"}},
              {{"date": "12-6-2024", "category": "Housing", "item": "Double A Batteries", "price": 750, "total": 8680, "currency": "LKR"}},
              {{"date": "12-6-2024", "category": "Shopping", "item": "Paper plates", "price": 350, "total": 8680, "currency": "LKR"}},
              {{"date": "12-6-2024", "category": "Shopping", "item": "Toilet paper roll", "price": 450, "total": 8680, "currency": "LKR"}},
              {{"date": "12-6-2024", "category": "Housing", "item": "Extension cord", "price": 5000, "total": 8680, "currency": "LKR"}}
          ]
        ```
    Type 2 Bill (Single-item):
       Example 1:
       ```
          [
              {{"date": "12-6-2024", "category": "Entertainment", "item": "Taylor Swift movie", "price": 2500, "total": 2500, "currency": "LKR"}}
          ]
        ```
       Example 2:
       ```
          [
              {{"date": "12-6-2024", "category": "Transportation", "item": "Air ticket", "price": 80, "total": 80, "currency": "USD"}}
          ]
        ```
    Do not provide anything other than the JSON.
    """

    # Generate response from the model
    response = model.generate_content(system_prompt)
    answer = response.text
    cleaned_text = re.sub(r"^```json|```$", "", answer.strip(), flags=re.MULTILINE)

    # Return the response
    return cleaned_text
