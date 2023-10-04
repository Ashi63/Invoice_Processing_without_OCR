import streamlit as st
from utils.db_operations import *
import subprocess


# Main Streamlit app
def main():
    st.title("Invoice Processing Automation")
    st.divider()

    # Create the user table if it doesn't exist
    create_user_table()

    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Login", "Sign-up"])

    if page == "Login":
        st.header("Login")
        identifier = st.text_input("Email or Username:")
        password = st.text_input("Password:", type="password")

        if st.button("Log In"):
            user = check_user(identifier, password)
            if user:
                st.success(f"Logged in as {user[1]} {user[2]}")  # Display username or email
                # Launch the "Invoice Processing App" in a new process
                st.success("Redirecting to Invoice Processing App...")
                subprocess.Popen(["streamlit", "run", "app_multi_page_.py"])
                return  # Exit the function
            else:
                st.error("Invalid credentials. Please try again.")

    elif page == "Sign-up":
        st.header("Sign-up")
        first_name = st.text_input("First Name:")
        last_name = st.text_input("Last Name:")
        company_name = st.text_input("Company Name:")
        email = st.text_input("Email:")
        new_username = st.text_input("Create Username:")
        new_password = st.text_input("Set Password:", type="password")

        if st.button("Sign Up"):
            if all([first_name, last_name, company_name, email, new_username, new_password]):
                insert_user(first_name, last_name, company_name, email, new_username, new_password)
                st.success("Account created. You can now log in.")
            else:
                st.warning("Please fill in all fields.")

if __name__ == '__main__':
    st.set_page_config(page_title="Login and Sign-up App", page_icon="🔐")
    main()