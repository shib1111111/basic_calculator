import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta
from streamlit_tags import st_tags, st_tags_sidebar

# Importing Firebase libraries for Authentication
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Setting up the Page Title and Icon
st.set_page_config(page_title="Expense Tracker", page_icon=":money_with_wings:")

# Setting up the Navigation Bar
menu = ["Home", "Login", "SignUp"]
choice = st.sidebar.selectbox("Menu", menu)

# Home Page
if choice == "Home":
    st.title("Welcome to Expense Tracker")
    st.write("Log in or Sign up to get started.")
    
# Login Page
elif choice == "Login":
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email)
            logged_in_user = auth.sign_in_with_email_and_password(email, password)
            st.success("Logged in as {}".format(email))
            
            # Creating a User Data Collection in Firestore
            user_data = db.collection(u'users').document(logged_in_user['localId'])
            if not user_data.get().exists:
                user_data.set({})
                
            # Redirecting to the Expense Tracking Page
            st.session_state.user = logged_in_user
            st.session_state.email = email
            st.session_state.user_data = user_data
            st.experimental_rerun()
            
        except auth.AuthError:
            st.error("Invalid Email or Password")

# Signup Page
elif choice == "SignUp":
    st.title("Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    if st.button("Sign Up"):
        if password == confirm_password:
            try:
                user = auth.create_user(email=email, password=password)
                st.success("Account created for {}".format(email))
                
                # Creating a User Data Collection in Firestore
                user_data = db.collection(u'users').document(user.uid)
                if not user_data.get().exists:
                    user_data.set({})
                
                # Redirecting to the Expense Tracking Page
                st.session_state.user = user
                st.session_state.email = email
                st.session_state.user_data = user_data
                st.experimental_rerun()
                
            except auth.AuthError as e:
                st.error(e.detail)
                
        else:
            st.error("Passwords do not match")

# Expense Tracking Page
if 'user' in st.session_state:
    st.title("Expense Tracker")
    st.write("Track your daily expenses here.")
    
    # Getting the User's Expense Data from Firestore
    user_data = st.session_state.user_data
    expenses = user_data.get().to_dict()
    
    # Creating an Empty Expense DataFrame
    columns = ['Date', 'Category', 'Description', 'Amount']
    expenses_df = pd.DataFrame(columns=columns)
    
    # Adding the Expense Data to the DataFrame
    if expenses:
        for date, data in expenses.items():
            for category, items in data.items():
                for item in items:
                    expenses_df = expenses_df.append(pd.Series([date, category,item['description'], item['amount']], index=columns), ignore_index=True)
    
    # Displaying the Expense Data in a Table
    st.write("## Expense Data")
    st.dataframe(expenses_df)
    
    # Getting the User Input for New Expenses
    st.write("## Add New Expense")
    date = st.date_input("Date")
    category = st_tags_sidebar("Select Category", ['Food', 'Housing', 'Transportation', 'Utilities', 'Entertainment', 'Other'])
    description = st.text_input("Description")
    amount = st.number_input("Amount", value=0.0, step=0.01)
    if st.button("Add Expense"):
        # Adding the Expense Data to Firestore
        expense_data = {
            'category': category,
            'description': description,
            'amount': amount
        }
        if str(date) in expenses:
            expenses[str(date)][category].append(expense_data)
        else:
            expenses[str(date)] = {category: [expense_data]}
        user_data.set(expenses)
        st.success("Expense added successfully")
        
    # Generating Expense Reports
    st.write("## Generate Expense Report")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if start_date <= end_date:
        # Creating a Filtered Expense DataFrame
        mask = (expenses_df['Date'] >= start_date) & (expenses_df['Date'] <= end_date)
        filtered_df = expenses_df.loc[mask]
        
        # Displaying the Filtered Expense Data in a Table
        st.write("### Expense Data for Selected Period")
        st.dataframe(filtered_df)
        
        # Generating a Pie Chart of Expense Categories
        fig = px.pie(filtered_df, values='Amount', names='Category')
        st.plotly_chart(fig)
        
        # Generating a Line Chart of Daily Expenses
        daily_expenses = filtered_df.groupby(['Date'])['Amount'].sum().reset_index()
        daily_expenses['Date'] = pd.to_datetime(daily_expenses['Date'])
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=daily_expenses['Date'], y=daily_expenses['Amount'], mode='lines+markers'))
        fig2.update_layout(title="Daily Expenses", xaxis_title="Date", yaxis_title="Amount")
        st.plotly_chart(fig2)
        
        # Providing Budgeting Advice
        total_expenses = filtered_df['Amount'].sum()
        days = (end_date - start_date).days + 1
        daily_budget = round(0.5 * total_expenses / days, 2)
        st.write("### Budgeting Advice")
        st.write("Total Expenses for Selected Period: $", round(total_expenses, 2))
        st.write("Daily Budget for Selected Period: $", daily_budget)
        if daily_expenses['Amount'].mean() > daily_budget:
            st.warning("You are spending more than your budget. Consider reducing your expenses.")
        else:
            st.success("You are within your budget. Keep it up!")
            
    else:
        st.error("Error: End Date must be after Start Date.")
        
    # Logging Out the User
    st.write("## Logout")
    if st.button("Logout"):
        auth.logout()
        st.experimental_rerun()

