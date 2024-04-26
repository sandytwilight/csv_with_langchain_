import pandas as pd
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd 
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
all_dataframes = []
# Function to read files from folder
def read_files_from_folder(folder_path):
    global all_dataframes 
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            # Read CSV file
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path,encoding='latin-1')
            print("file read suuu")
            all_dataframes.append(df)
        elif file_name.endswith('.xlsx'):
            # Convert Excel to CSV and then read CSV
            excel_file_path = os.path.join(folder_path, file_name)
            csv_file_path = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}.csv")
            # Convert Excel to CSV
            excel_data = pd.read_excel(excel_file_path,encoding='latin-1')
            excel_data.to_csv(csv_file_path, index=False)
            # Read CSV
            df = pd.read_csv(csv_file_path)
            print("file read suuu")
            all_dataframes.append(df)
    return pd.concat(all_dataframes, ignore_index=True)

# Provide the folder path
folder_path = r"F:\DATASET"

# Read all files from folder and store into one DataFrame
combined_df = read_files_from_folder(folder_path)

d2=all_dataframes
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyAHqjWfhY9OULDJbJm1Jt6vgxzMAlWdohE"

model = ChatGoogleGenerativeAI(model='gemini-pro',TEMPERATURE=0)
# response = model.generate_content("Write a story about a magic backpack.")
# print(response.text)
pd_agent = create_pandas_dataframe_agent(model, all_dataframes, verbose=True)
pd_agent2 = create_pandas_dataframe_agent(model, all_dataframes, verbose=True)
# pd_agent = create_pandas_dataframe_agent(model, data, verbose=True)

# res=csv_agent.run("ride type")
res=pd_agent.run("which bank is having highest fund and that bank name")
res2=pd_agent2.run("which bank is having highest fund and that bank name")
print(res)
print(res2)