import streamlit as st
from functions import load_data, display_category_items


def add_sidebar(image_path):
    with st.sidebar:
        st.markdown("---")
        st.image(image_path, use_container_width=True)
        st.markdown("---")


def main():
    # add_sidebar("/content/2.png")

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

    _, category_totals, _ = load_data()

    category_totals = {
        cat: category_totals.get(cat, 0) for cat in predefined_categories
    }

    st.header("Automated Expense Management System")

    # Spending summary with thresholds
    thresholds = st.session_state.get("thresholds", {})
    max_threshold = st.session_state.get("max_threshold", 200000)

    for category in predefined_categories:
        if category not in thresholds:
            thresholds[category] = int((max_threshold * 0.1))

    for category in predefined_categories:
        total = category_totals[category]
        threshold = thresholds.get(category, float("inf"))
        # description = spending_description(total, threshold)
        box_color = "green" if total <= threshold else "red"
        box_style = f"border: 2px solid {box_color}; padding: 15px; border-radius: 10px; margin-bottom: 10px;"

        # Display descriptive box
        with st.container():
            st.markdown(
                f"""
                <div style="{box_style}">
                    <h4 style="margin: 0; color: {box_color};">{category}</h4>
                    <p>
                    <span style="background-color: #fbe9e7; padding: 5px 10px; border-radius: 5px; font-weight: bold; color: #FF5722;">💰 Spent: LKR {total}</span>
                    <span style="background-color: #e0f7fa; padding: 5px 10px; border-radius: 5px; font-weight: bold; color: #4CAF50;">💸 Allowed: LKR {threshold}</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Alert if spending exceeds threshold
            if total > threshold:
                st.error(
                    f"⚠️ **Alert!** {category} spending (LKR {total}) exceeds the threshold (LKR {threshold}) by LKR {total - threshold}!"
                )

        # Expandable section for category items
        with st.expander(f"View {category} items"):
            category_items = display_category_items(category)
            if category_items:
                for item in category_items:
                    st.write(
                        f"- Item: **{item['item']}**, Price: **LKR {item['price']}**"
                    )
            else:
                st.write("No items found for this category.")
