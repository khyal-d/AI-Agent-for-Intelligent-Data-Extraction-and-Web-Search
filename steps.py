import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
import gspread
from google.oauth2.service_account import Credentials
import requests  # For calling the Groq API
import os
from dotenv import load_dotenv

# set GROQ_API_KEY=<key>, iss ko cmd me daalo
# This command will set the GROQ_API_KEY for the current Command Prompt session. 
# Please note that this setting will only last 
# as long as the Command Prompt window is open. 
# Once you close it, the variable will be lost.


# Check if the SERPAPI_KEY environment variable is set

load_dotenv()  # Load environment variables from .env
api_key = os.getenv('GROQ_API_KEY')
if api_key:
    print(f"Your API key is: {api_key}")
else:
    print("SERPAPI_KEY is not set.")
    
# Function to perform web search
def perform_web_search(query):
    params = {
        "engine": "google",
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": os.getenv("SERPAPI_KEY")  # Retrieves the API key from the environment variable
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get('organic_results', [])

# Function to send results to the Groq API for parsing
def send_to_groq(results, prompt):
    groq_api_url = 'GROQ_API_ENDPOINT'
    headers = {'Authorization': 'Bearer GROQ_API_KEY'}
    data = {
        'prompt': prompt,
        'results': results
    }
    response = requests.post(groq_api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Assuming the Groq API returns JSON data
    else:
        return {"error": "Failed to retrieve data from Groq API"}

def convert_to_direct_download_link(drive_link):
    """Convert Google Drive link to direct download link."""
    file_id = drive_link.split('/d/')[1].split('/')[0]
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Streamlit app
st.title("Dashboard for File Upload and Google Sheets Connection")

# File Upload Section
st.header("Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.dataframe(df)

    # Select the main column
    main_column = st.selectbox("Select the main column:", df.columns)
    st.write(f"Selected Main Column: {main_column}")

    # Dynamic Query Input for Uploaded CSV Data
    st.header("Dynamic Query Input for Uploaded CSV Data")
    prompt_template = st.text_input("Define your custom prompt (use placeholders like {entity}):", f"Get me the email address of {{entity}} (selected column: {main_column})")
    
    if st.button("Generate Queries from CSV"):
        if df is not None and main_column in df.columns:
            queries = [prompt_template.format(entity=row[main_column]) for index, row in df.iterrows()]
            st.write("Generated Queries from CSV:")
            st.write(queries)
        else:
            st.warning("Please ensure you have selected a valid main column.")

        # Perform web searches for each query
        search_results = {}
        extracted_info = []  # To store extracted information
        for query in queries:
            search_results[query] = perform_web_search(query)

        # Display search results and send to Groq API
        for query, results in search_results.items():
            st.subheader(f"Results for: {query}")
            for result in results:
                st.write(f"**Title:** {result.get('title')}")
                st.write(f"**Link:** [Click Here]({result.get('link')})")
                st.write(f"**Snippet:** {result.get('snippet')}")
                st.write("---")

            # Send results to Groq API for parsing
            groq_response = send_to_groq(results, prompt_template.format(entity=query))
            st.write("Groq Response:", groq_response)

            # Store the extracted information
            if "extracted_info" in groq_response:  # Assuming your Groq API responds with extracted information
                extracted_info.append({
                    "query": query,
                    "extracted_data": groq_response["extracted_info"]
                })

        # Display extracted information
        st.header("Extracted Information")
        if extracted_info:
            for item in extracted_info:
                st.write(f"**Query:** {item['query']}")
                st.write(f"**Extracted Data:** {item['extracted_data']}")
                st.write("---")

        # 'extracted_info' contains the data you want to download
        if extracted_info:
            st.header("Extracted Information")
            results_data = []  # List to hold the data for the CSV

            for item in extracted_info:
                st.write(f"**Query:** {item['query']}")
                st.write(f"**Extracted Data:** {item['extracted_data']}")
                st.write("---")
                
                # Append data to results_data for CSV
                results_data.append({
                    "Query": item['query'],
                    "Extracted Data": item['extracted_data']
                })

            # Create a DataFrame from the results
            results_df = pd.DataFrame(results_data)

            # Provide an option to download the results as CSV
            csv = results_df.to_csv(index=False)  # Convert DataFrame to CSV
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name='search_results.csv',
                mime='text/csv',
            )



# Google Sheets Connection Section
st.header("Connect to Google Sheet")

sample_data_url = st.text_input("Enter URL of a CSV file or direct download link from drive (public):")

if sample_data_url:
    # Check if the provided link is a Google Drive link
    if "drive.google.com" in sample_data_url:
        direct_link = convert_to_direct_download_link(sample_data_url)
    else:
        direct_link = sample_data_url  # Use as is if it's already a direct link

    try:
        # Read the CSV from the provided URL
        df_sample = pd.read_csv(direct_link)
        st.write("Preview of Sample Data:")
        st.dataframe(df_sample)

        # Select the main column from the sample data
        main_column_sample = st.selectbox("Select the main column from Sample Data:", df_sample.columns)
        st.write(f"Selected Main Column from Sample Data: {main_column_sample}")
    except Exception as e:
        st.error(f"Error loading sample data: {e}")
