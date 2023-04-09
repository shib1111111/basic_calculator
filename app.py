import streamlit as st
import calculator_logic

st.title("Calculator App")

num1 = st.number_input("Enter the first number:")
num2 = st.number_input("Enter the second number:")
operation = st.selectbox("Select an operation", calculator_logic.OPERATIONS)

if st.button("Calculate"):
    result = calculator_logic.calculate(num1, num2, operation)
    st.success(f"The result is {result}")

    
    
    

# Define a function to display the signature
def display_signature():
    st.markdown(
        """
        <style>
        .signature {
            font-size: 1rem;
            font-style: italic;
            text-align: center;
            padding: 1rem 0;
            color: #333;
            transition: color 0.5s ease-in-out;
        }
        .signature:hover {
            color: #007bff;
        }
        </style>
        """
        , unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="signature">
        Made with ❤️ by Shib Kumar Saraf
        </div>
        """
        , unsafe_allow_html=True
    )

# Add the signature to your Streamlit app
display_signature()
