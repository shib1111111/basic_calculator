import streamlit as st
import calculator_logic

st.title("Calculator App")

num1 = st.number_input("Enter the first number:")
num2 = st.number_input("Enter the second number:")
operation = st.selectbox("Select an operation", calculator_logic.OPERATIONS)

if st.button("Calculate"):
    result = calculator_logic.calculate(num1, num2, operation)
    st.success(f"The result is {result}")
