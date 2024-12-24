import os
import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image
import json
from process_image import process_image_with_document_ai
from process_data import process_bill_data
from currency_converter import convert_currency
from db import add_expense, add_new_cycle, get_expenses_by_cycle
from db import session, Expense, SpendingCycle
from dotenv import load_dotenv

load_dotenv()

config = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
}

file_path = "data.json"
with open(file_path, "w") as json_file:
    json.dump(config, json_file, indent=4)

def add_sidebar(image_path):
    with st.sidebar:
        st.markdown("---")
        st.image(image_path, use_container_width=True)
        st.markdown("---")


def main():
    # add_sidebar("/content/4.png")
    # Page Title
    # st.header("Expense Hub")

    # Section Tabs
    tab1, tab2, tab3 = st.tabs(["Physical Bills", "E-Bills", "Manual Entries"])

    # Tab 1: Physical Bills
    with tab1:
        if "view_pressed" not in st.session_state:
            st.session_state.view_pressed = False

        # # Reset session state when uploading a new file or making a new action
        # if st.button("Upload New File"):
        #     # Reset session states
        #     st.session_state.view_pressed = False
        #     st.session_state.data = None
        #     st.session_state.selected_date = None
        #     st.session_state.uploaded_file = None

        selected_date = st.date_input(
            "Date", value=datetime.now().date(), key="date_physical"
        )

        st.subheader("Scan and Upload")
        uploaded_file = st.file_uploader(
            "Supported formats: JPEG, JPG, PNG, BMP, PDF, TIFF, TIF, GIF",
            type=["jpeg", "jpg", "png", "bmp", "pdf", "tiff", "tif", "gif"],
        )

        # Display Uploaded File
        if uploaded_file:
            file_type = uploaded_file.type
            file_path = f"uploaded_files/{uploaded_file.name}"

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the uploaded file to the local path
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if "image" in file_type:  # If the uploaded file is an image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", width=500)
            elif file_type == "application/pdf":  # If it's a PDF
                st.write("PDF uploaded successfully.")
            else:  # For other file types
                st.write(
                    f"{file_type.split('/')[-1].upper()} file uploaded successfully."
                )

        if st.button("Submit", key="submit_physical"):
            if uploaded_file:
                st.success(f"File uploaded on {selected_date} successfully!")
                input_variables = process_image_with_document_ai(
                    project_id="expense-manager-443707",
                    location="us",
                    processor_id="b84e8cb603801976",
                    file_path=file_path,
                    key_path="data.json",
                )
                input_variables["date"] = selected_date

                st.session_state.data = process_bill_data(
                    input_variables, api_key=os.getenv("API_KEY")
                )
                # st.write(st.session_state.data)
                st.session_state.view_pressed = True  # Activate View button state
            else:
                st.error("Please upload a file before submitting.")

        if "data" in st.session_state:
            data = st.session_state.data

        # Show table when View button is pressed
        if st.session_state.view_pressed:
            st.write("Review and Edit Details:")
            if data:
                data_parsed = json.loads(data)

                try:
                    df = pd.DataFrame(data_parsed)
                    df = df.rename(
                        columns={
                            "item": "Item",
                            "category": "Category",
                            "price": "Price",
                            "date": "Date",
                            "total": "Total",
                            "currency": "Currency",
                        }
                    )
                except json.JSONDecodeError as e:
                    st.error(f"Error decoding JSON: {e}")
            else:
                st.write("No data available to display.")

            bill_date = st.date_input(
                "Date", value=pd.to_datetime(df["Date"].iloc[0]).date(), key="bill_date"
            )
            # formatted_date = bill_date.strftime("%Y-%m-%d")
            # 'st.write(f"Formatted Date: {formatted_date}")

            currency = (st.text_input("Currency", value=df["Currency"].iloc[0])).upper()

            total_value=float(df["Total"].iloc[0])
            st.number_input("Bill Total", value=total_value)

            # Initialize columns for both the original and converted prices
            df["Original Price"] = df["Price"]  # Keep the original price
            total_original = float(df["Total"].iloc[0])
            total_in_lkr = None

            if currency != "LKR":
                df["Price in LKR"] = df["Price"].apply(
                    lambda x: convert_currency(currency, "LKR", x)
                )
                total_in_lkr = convert_currency(currency, "LKR", total_original)
            col1, col2 = st.columns(2)
            col1.metric(
                label=f"Total Bill ({currency})",
                value=f"{total_original:.2f} {currency}",
            )
            if total_in_lkr is not None:
                col2.metric(label="Total Bill (LKR)", value=f"{total_in_lkr:.2f} LKR")

            # Show the editable table
            df = df.drop(columns=["Date", "Total", "Currency"])

            if "Price in LKR" in df.columns:
                df = df[
                    ["Category", "Item", "Original Price", "Price in LKR"]
                ]  # Show only relevant columns
            else:
                df = df[
                    ["Category", "Item", "Original Price"]
                ]  # If no conversion, show just the original price

            edited_df = st.data_editor(df, num_rows="dynamic")

            if st.button("Confirm"):
                df_final = pd.DataFrame(
                    {
                        "Date": [bill_date] * len(edited_df),
                        "Category": edited_df["Category"],
                        "Item": edited_df["Item"],
                        "Price": edited_df["Original Price"],
                        "Currency": [currency] * len(edited_df),
                    }
                )

                cycle_id = add_new_cycle(
                    start_date=selected_date
                )  # Add a new spending cycle
                for _, row in df_final.iterrows():
                    add_expense(
                        category=row["Category"],
                        price=row["Price"],
                        date=selected_date,
                        cycle_id=cycle_id,
                        currency=row["Currency"],
                    )
                st.success("Details confirmed & added to the database!")

    # Tab 2: E-Bills
    with tab2:
        selected_date = st.date_input(
            "Date", value=datetime.now().date(), key="date_ebill"
        )

        st.subheader("Digital Receipts")
        e_bill_text = st.text_area(
            "Copy and paste your digital receipt details below:", height=150
        )

        if st.button("Submit", key="submit_ebill"):
            if e_bill_text:
                st.success(f"Receipt submitted on {selected_date} successfully!")
            else:
                st.error("Please insert a receipt before submitting.")

    # Tab 3: Manual Entry
    with tab3:
        selected_date = st.date_input(
            "Date", value=datetime.now().date(), key="date_manual"
        )

        st.subheader("Manual Entries")
        categories = [
            "Food",
            "Transportation",
            "Housing",
            "Shopping",
            "Healthcare",
            "Entertainment",
            "Others",
        ]
        selected_category = st.selectbox("Select Expense Category", categories)

        st.subheader("Add Items (Optional)")

        if "expenses_df" not in st.session_state:
            st.session_state.expenses_df = pd.DataFrame(
                columns=["Item Name", "Item Price"]
            )

        with st.form(key="expense_form"):
            for i in range(len(st.session_state.expenses_df)):
                row = st.session_state.expenses_df.iloc[i]
                item_name = st.text_input(
                    f"Item {i+1} Name", value=row["Item Name"], key=f"item_name_{i}"
                )
                item_price = st.number_input(
                    f"Item {i+1} Price",
                    value=row["Item Price"],
                    key=f"item_price_{i}",
                    min_value=0.0,
                    step=0.01,
                )

                st.session_state.expenses_df.at[i, "Item Name"] = item_name
                st.session_state.expenses_df.at[i, "Item Price"] = item_price

            if st.form_submit_button("Add More Items"):
                st.session_state.expenses_df = pd.concat(
                    [
                        st.session_state.expenses_df,
                        pd.DataFrame([{"Item Name": "", "Item Price": 0.0}]),
                    ],
                    ignore_index=True,
                )

        calculated_total = st.session_state.expenses_df["Item Price"].sum()

        st.subheader("Total Expense")
        total_amount = st.number_input(
            "Enter Total Amount Spent (Auto-calculated if items are added):",
            min_value=float(calculated_total),
            value=float(calculated_total),
            step=0.01,
        )

        if st.button("Submit Manual Entry", key=33):
            if total_amount > 0:
                st.success(
                    f"Manual entry submitted successfully for category '{selected_category}'!"
                )
            else:
                st.error("Please provide at least one item or enter a total amount.")


if __name__ == "__main__":
    main()
