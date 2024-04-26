import streamlit as st
import pandas as pd
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Function to read files from folder
def read_files_from_folder(folder_path):
    all_dataframes = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            # Read CSV file
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            all_dataframes.append(df)
        elif file_name.endswith('.xlsx'):
            # Convert Excel to CSV and then read CSV
            excel_file_path = os.path.join(folder_path, file_name)
            csv_file_path = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}.csv")
            # Convert Excel to CSV
            excel_data = pd.read_excel(excel_file_path)
            excel_data.to_csv(csv_file_path, index=False)
            # Read CSV
            df = pd.read_csv(csv_file_path)
            all_dataframes.append(df)
    return pd.concat(all_dataframes, ignore_index=True)

# Create Streamlit app
st.title("CHAT WITH CSV AND EXCEL")

# Sidebar for folder input
st.sidebar.header("Folder Input")
folder_path = st.sidebar.text_input(r"Enter folder path:")

# Check if folder path is provided
if folder_path:
    # Read all files from folder and store into one DataFrame
    try:
        combined_df = read_files_from_folder(folder_path)
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
    else:
        # Set up Google API key
        os.environ["GOOGLE_API_KEY"] = "AIzaSyAHqjWfhY9OULDJbJm1Jt6vgxzMAlWdohE"

        # Initialize Google Generative AI model
        model = ChatGoogleGenerativeAI(model='gemini-pro', TEMPERATURE=0)

        # Sidebar for user input
        st.sidebar.header("User Input")
        query = st.sidebar.text_input("Enter your query:")

        # Run query when button is clicked
        if st.sidebar.button("Run Query"):
            # Create agent with Google Generative AI
            pd_agent = create_pandas_dataframe_agent(model, combined_df, verbose=True)
            
            # Run query through the agent
            res = pd_agent.run(query)
            
            # Display result
            st.subheader("Result:")
            st.write(res)
else:
    st.sidebar.info("Please enter a folder path.")
