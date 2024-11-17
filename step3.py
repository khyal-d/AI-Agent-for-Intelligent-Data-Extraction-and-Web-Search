import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
from serpapi import GoogleSearch

# Setup Google Sheets connection
def google_sheet_connect(sheet_url):
    credentials = Credentials.from_service_account_file('path/to/your/service_account.json')
    gc = gspread.authorize(credentials)
    return gc.open_by_url(sheet_url).get_worksheet(0).get_all_records()

# import os
# Check if the SERPAPI_KEY environment variable is set
api_key = os.getenv("SERPAPI_KEY")
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
    # prompt_template = prompt_template.dropna(axis=1, how='all')
    if st.button("Generate Queries from CSV"):
        if df is not None and main_column in df.columns:
            queries = [prompt_template.format(entity=row[main_column]) for index, row in df.iterrows()]
            st.write("Generated Queries from CSV:")
            st.write(queries)
        else:
            st.warning("Please ensure you have selected a valid main column.")

        # Perform web searches for each query
        search_results = {}
        for query in queries:
            search_results[query] = perform_web_search(query)

        # Display search results
        for query, results in search_results.items():
            st.subheader(f"Results for: {query}")
            for result in results:
                st.write(f"**Title:** {result.get('title')}")
                st.write(f"**Link:** [Click Here]({result.get('link')})")
                st.write(f"**Snippet:** {result.get('snippet')}")
                st.write("---")

# Google Sheets Connection Section
st.header("Connect to Google Sheet")
sheet_url = st.text_input("Enter Google Sheet URL:")

if sheet_url:
    try:
        google_data = google_sheet_connect(sheet_url)
        df_google = pd.DataFrame(google_data)
        st.write("Preview of Google Sheet Data:")
        st.dataframe(df_google)

        # Select the main column from Google Sheet
        main_column_google = st.selectbox("Select the main column from Google Sheet:", df_google.columns)
        st.write(f"Selected Main Column from Google Sheet: {main_column_google}")

        # Dynamic Query Input for Google Sheet Data
        prompt_template_google = st.text_input("Define your custom prompt for Google Sheet (use placeholders like {entity}):", "Get me the email address of {company}")
        
        if st.button("Generate Google Queries"):
            # Generate queries based on the selected main column from Google Sheet
            google_queries = [prompt_template_google.format(entity=row[main_column_google]) for index, row in df_google.iterrows()]
            st.write("Generated Google Queries:")
            st.write(google_queries)

            # Perform web searches for each Google query
            google_search_results = {}
            for query in google_queries:
                google_search_results[query] = perform_web_search(query)

            # Display Google search results
            for query, results in google_search_results.items():
                st.subheader(f"Results for: {query}")
                for result in results:
                    st.write(f"**Title:** {result.get('title')}")
                    st.write(f"**Link:** [Click Here]({result.get('link')})")
                    st.write(f"**Snippet:** {result.get('snippet')}")
                    st.write("---")

    except Exception as e:
        st.error(f"Error connecting to Google Sheet: {e}")



