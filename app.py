import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.set_page_config(page_title="ANOVA Analysis Tool")

# Define app function
def app():
    # Add a title
    st.title("ANOVA Analysis Tool")

    # Add a file uploader so the user can upload a CSV or Excel file
    st.write("Upload your data:")
    data_file = st.file_uploader("Select a CSV or Excel file", type=["csv", "xlsx"])
    st.markdown("Or")
    st.write("Enter your data manually:")

    num_rows = st.number_input("Number of rows", value=5, min_value=1, max_value=100)
    num_cols = st.number_input("Number of columns", value=5, min_value=1, max_value=100)

    st.info("Please upload a CSV or Excel file or enter your data manually in the text boxes provided.")

    # Create empty dataframe
    df = pd.DataFrame()

    # If the user has uploaded a file, use the file data to create the dataframe
    if data_file:
        try:
            if data_file.name.endswith(".csv"):
                df = pd.read_csv(data_file)
            else:
                df = pd.read_excel(data_file)
        except:
            st.error("Error: Invalid file format or file contents")
            return

    # If the dataframe is still empty, get the data from the user input
    if df.empty:
        data = [[st.number_input(f"Row {i+1}, Column {j+1}", value=0.0) for j in range(num_cols)] for i in range(num_rows)]
        df = pd.DataFrame(data, columns=[f"Column {j+1}" for j in range(num_cols)])

    # Display the data as a table
    st.write("Data:")
    st.dataframe(df)

    # Add a button to perform the ANOVA analysis
    if st.button("Perform ANOVA Analysis"):
        # Allow the user to select the dependent and independent variables
        dep_variable = st.selectbox("Select dependent variable", df.columns)
        ind_variable = st.multiselect("Select independent variables", df.columns, default=[df.columns[0]])
        st.info("Please select the dependent and independent variables to perform the analysis.")

        # Perform ANOVA analysis using statsmodels
        X = sm.add_constant(df[ind_variable])
        model = sm.OLS(df[dep_variable], X).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)

        # Display the ANOVA table
        st.write("ANOVA Table:")
        st.dataframe(anova_table)

        # Get the R-squared value and display it
        r_squared = model.rsquared
        st.write(f"R-squared value: {r_squared:.2f}")

        # Plot the dependent variable against each independent variable
        for variable in ind_variable:
            fig, ax = plt.subplots()
            sns.scatterplot(x=variable, y=dep_variable, data=df, ax=ax)
            st.pyplot(fig)

# Run the app
app()
