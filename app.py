# https://easytrack-hwxv9npods3gyzbowyzehh.streamlit.app/

import streamlit as st
from streamlit_option_menu import option_menu
import home
import settings
import analytics
import exp_app
from sidebar import add_sidebar

# Set page configuration
st.set_page_config(
    page_title="EasyTrack",
    layout="wide",
)


# Authentication check
def check_login(username, password):
    # Replace these credentials with your actual authentication backend
    return username == "abcd" and password == "1234"


# Login Page
def login_page():
    st.title("Welcome to EasyTrack!")
    add_sidebar("Images/login.png")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.session_state["authenticated"] = True
            st.session_state["current_page"] = (
                "Settings"  # Set the default page after login
            )
            # st.experimental_set_query_params(dummy=str(st.session_state["authenticated"]))
            st.query_params = {"page": "Settings"}
            st.session_state["login"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")


# Main App
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Login"

# Ensure we use session_state to track pages
if "login" in st.session_state and st.session_state["login"]:
    query_params = st.query_params
    if "page" in query_params:
        st.session_state["current_page"] = query_params["page"]

# query_params = st.query_params
# if "page" in query_params:
#     st.session_state["current_page"] = query_params["page"]

if not st.session_state["authenticated"]:
    st.session_state["current_page"] = "Login"
    login_page()
else:
    # Navigation Menu
    menu = option_menu(
        menu_title=None,
        options=["Settings", "Dashboard", "Expense Hub", "Insights"],
        icons=["gear", "house", "wallet", "bar-chart"],
        menu_icon="cast",
        default_index=["Settings", "Dashboard", "Expense Hub", "Insights"].index(
            st.session_state["current_page"]
        ),
        orientation="horizontal",
        styles={
            "container": {
                "padding": "5px",
                "background-color": "#f0f2f6",
            },  # Adjust container padding and background
            "icon": {"color": "#3e8a56", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "10px",
                "color": "#000",
            },
            "nav-link-selected": {
                "background-color": "#f00",
                "color": "#fff",
            },  # Highlight selected menu item
        },
    )
    st.session_state["current_page"] = menu  # Track the current page
    # st.query_params = {"page": menu}
    st.session_state["login"] = False

    # Load the appropriate page based on user selection
    if menu == "Settings":
        settings.add_sidebar("Images/1.png")
        settings.main()
    elif menu == "Dashboard":
        home.add_sidebar("Images/4.png")
        home.main()
    elif menu == "Expense Hub":
        exp_app.add_sidebar("Images/3.png")
        exp_app.main()
    elif menu == "Insights":
        analytics.add_sidebar("Images/2.png")
        analytics.main()
