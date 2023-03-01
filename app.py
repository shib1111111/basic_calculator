import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import smtplib
def calculate_expenses(data):
    # Get the current date and time
    now = datetime.datetime.now()
    
    # Add the current date and time to the data
    data["Date"] = now.date()
    data["Time"] = now.time()
    
    # Calculate the total expense for the day
    total = data["Amount"].sum()
    
    # Load the previous expenses from the CSV file
    try:
        expenses = pd.read_csv("expenses.csv", index_col=0)
    except FileNotFoundError:
        expenses = pd.DataFrame(columns=["Date", "Time", "Amount"])
    
    # Add the new expenses to the DataFrame
    expenses = pd.concat([expenses, data], ignore_index=True)
    
    # Save the updated expenses to the CSV file
    expenses.to_csv("expenses.csv")
    
    return total
  st.title("Daily Expense Calculator")

# Get the user's input data
amount = st.number_input("Enter the amount")
category = st.text_input("Enter the category")
description = st.text_input("Enter the description")

# Create a dictionary with the input data
data = {"Category": category, "Description": description, "Amount": amount}
# Allow the user to calculate their expenses
if st.button("Calculate"):
    total = calculate_expenses(pd.DataFrame(data, index=[0]))
    st.write("You have spent $", total, "today.")
    
    # Plot the daily spending over time
    expenses = pd.read_csv("expenses.csv", index_col=0)
    expenses["Date"] = pd.to_datetime(expenses["Date"])
    daily_expenses = expenses.groupby("Date")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.plot(daily_expenses)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total expenses")
    st.pyplot(fig)
# Provide feedback on budget maintenance
if "expenses" in locals():
    daily_budget = st.number_input("Enter your daily budget", value=100)
    today = datetime.datetime.now().date()
    today_expenses = expenses[expenses["Date"] == today]["Amount"].sum()
    today_budget = daily_budget - today_expenses
    if today_budget >= 0:
        st.write("You have $", today_budget, "left in your daily budget.")
    else:
        st.write("You have exceeded your daily budget by $", abs(today_budget), ".")
# Log out and send email
if st.button("Logout"):
    email = st.text_input("Enter your email address")
    password
