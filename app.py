import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import smtplib

def calculate_expenses(data):
    now = datetime.datetime.now()
    data["Date"] = now.date()
    data["Time"] = now.time()
    total = data["Amount"].sum()
    try:
        expenses = pd.read_csv("expenses.csv", index_col=0)
    except FileNotFoundError:
        expenses = pd.DataFrame(columns=["Date", "Time", "Amount"])
    expenses = pd.concat([expenses, data], ignore_index=True)
    expenses.to_csv("expenses.csv")
    return total

def send_email(email, password, subject, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, f"Subject: {subject}\n\n{message}")
    server.quit()

st.title("Daily Expense Calculator")

amount = st.number_input("Enter the amount")
category = st.text_input("Enter the category")
description = st.text_input("Enter the description")

data = {"Category": category, "Description": description, "Amount": amount}

if st.button("Calculate"):
    total = calculate_expenses(pd.DataFrame(data, index=[0]))
    st.write("You have spent $", total, "today.")
    
    expenses = pd.read_csv("expenses.csv", index_col=0)
    expenses["Date"] = pd.to_datetime(expenses["Date"])
    daily_expenses = expenses.groupby("Date")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.plot(daily_expenses)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total expenses")
    st.pyplot(fig)

if "expenses" in locals():
    daily_budget = st.number_input("Enter your daily budget", value=100)
    today = datetime.datetime.now().date()
    today_expenses = expenses[expenses["Date"] == today]["Amount"].sum()
    today_budget = daily_budget - today_expenses
    if today_budget >= 0:
        st.write("You have $", today_budget, "left in your daily budget.")
    else:
        st.write("You have exceeded your daily budget by $", abs(today_budget), ".")

if st.button("Logout"):
    email = st.text_input("Enter your email address")
    password = st.text_input("Enter your email password", type="password")
    subject = "Daily Expenses"
    message = pd.read_csv("expenses.csv").to_string()
    send_email(email, password, subject, message)
    st.write("Your daily expenses have been sent to your email.")
