import streamlit as st
import plotly.express as px
import pandas as pd
from functions import load_data


def add_sidebar(image_path):
    with st.sidebar:
        st.markdown("---")
        st.image(image_path, use_container_width=True)
        st.markdown("---")


def main():
    # add_sidebar("/content/4.png")

    # Load data dynamically
    predefined_categories = [
        "Food",
        "Transportation",
        "Housing",
        "Shopping",
        "Healthcare",
        "Entertainment",
        "Other",
    ]

    df, category_totals, _ = load_data()

    for category in predefined_categories:
        if category not in df["category"].unique():
            df = df.append(
                {"category": category, "cumulative_sum": 0, "date": None},
                ignore_index=True,
            )

    st.header("Spending Insights")

    # Bar chart for category-wise total spending
    # st.subheader("Total Spending by Category")
    if not df.empty:
        bar_data = pd.DataFrame(
            list(category_totals.items()), columns=["category", "category_totals"]
        )
        bar_data = bar_data[bar_data["category"].isin(predefined_categories)]
        # bar_data = df.groupby("category")["cumulative_sum"].sum().reset_index()
        fig = px.bar(
            bar_data,
            x="category",
            y="category_totals",
            title="Total Spending by Category",
            labels={"category_totals": "Amount Spent (LKR)", "category": "Category"},
            color="category",
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.write("No data available to plot.")

    # Line chart for category-wise spending trends
    # st.subheader("Category-wise Spending Over Time")
    if not df.empty:
        fig = px.line(
            df,
            x="date",
            y="cumulative_sum",
            color="category",
            title="Spending Trends by Category",
            labels={
                "cumulative_sum": "Amount Spent (LKR)",
                "date": "Date",
                "category": "Category",
            },
            markers=True,
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig)
    else:
        st.write("No data available to plot.")

        # Add download button for CSV export
    st.download_button(
        label="Download Analytics Data",
        data=df.to_csv(index=False),  # Convert the DataFrame to CSV format
        file_name="analytics_data.csv",  # File name for the downloaded CSV
        mime="text/csv",  # MIME type for CSV
    )
