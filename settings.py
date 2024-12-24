import streamlit as st
from datetime import datetime, timedelta
from functions import update_settings


def add_sidebar(image_path):
    with st.sidebar:
        st.markdown("---")
        st.image(image_path, use_container_width=True)
        st.markdown("---")


def main():
    # add_sidebar("/content/1.png")
    st.header("Settings")

    # Spending cycle start date
    start_date = st.date_input(
        "Select Spending Cycle Start Date",
        value=st.session_state.get("start_date", datetime.now()),
        help="This is the date when the monthly spending cycle starts.",
    )

    if "start_date" not in st.session_state:
        st.session_state.start_date = start_date

    # Monthly spending limit
    max_threshold = st.number_input(
        "Enter Maximum Limit (LKR)",
        min_value=10000,
        max_value=500000,
        value=st.session_state.get("max_threshold", 200000),
        step=1000,
    )

    if "max_threshold" not in st.session_state:
        st.session_state.max_threshold = max_threshold

    # Time period selection
    time_period_options = {
        "1 Week": 7,
        "2 Weeks": 14,
        "1 Month": 30,
        "2 Months": 60,
    }

    selected_period = st.selectbox(
        "Select Time Period",
        options=list(time_period_options.keys()),
        help="Select the duration for your spending cycle.",
    )

    # Calculate cycle end date
    cycle_end_date = start_date + timedelta(days=time_period_options[selected_period])

    # Display cycle end date
    st.write(f"Cycle End Date: {cycle_end_date.strftime('%Y-%m-%d')}")

    category_percentages = {
        "Food": 25,
        "Housing": 25,
        "Shopping": 15,
        "Entertainment": 10,
        "Healthcare": 10,
        "Transportation": 5,
        "Other": 10,
    }

    # Adjust category limits
    st.subheader("Adjust Category Limits")
    if "thresholds" not in st.session_state:
        st.session_state.thresholds = {}
    # st.write("Thresholds State:", st.session_state.thresholds)

    for category, percentage in category_percentages.items():
        # Ensure valid initialization
        if category not in st.session_state.thresholds or not isinstance(
            st.session_state.thresholds[category], (int, float)
        ):
            st.session_state.thresholds[category] = int(
                (max_threshold * percentage) / 100 * 0.7
            )

        # Ensure finite value
        current_value = st.session_state.thresholds[category]
        if current_value == float("inf"):
            current_value = int((max_threshold * percentage) / 100 * 0.7)
            st.session_state.thresholds[category] = current_value

        # Slider
        st.session_state.thresholds[category] = st.slider(
            f"{category} (LKR)",
            min_value=0,
            max_value=int((max_threshold * percentage) / 100),
            value=current_value,
            step=1000,
        )

    # Save settings
    if st.button("Save Settings"):
        st.session_state.start_date = start_date
        st.session_state.max_threshold = max_threshold
        update_settings(start_date, max_threshold, st.session_state.thresholds)
        st.success("Settings saved successfully!")
