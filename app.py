import streamlit as st
import pandas as pd
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
    data_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    # If a file has been uploaded, display the data and perform ANOVA analysis
    if data_file:
        df = pd.read_csv(data_file) if data_file.name.endswith(".csv") else pd.read_excel(data_file)

        # Display the data as a table
        st.write("Data:")
        st.dataframe(df)

        # Allow the user to select the dependent and independent variables
        dep_variable = st.selectbox("Select dependent variable", df.columns)
        ind_variable = st.multiselect("Select independent variables", df.columns, default=[df.columns[0]])

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
