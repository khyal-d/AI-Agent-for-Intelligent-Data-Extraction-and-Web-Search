import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from serpapi import GoogleSearch
import requests  # For calling the Groq API

# Setup Google Sheets connection
def google_sheet_connect(sheet_url):
    credentials = Credentials.from_service_account_file('/absolute/path/to/your/service_account.json')
    gc = gspread.authorize(credentials)
    return gc.open_by_url(sheet_url).get_worksheet(0).get_all_records()

# Function to perform web search
def perform_web_search(query):
    params = {
        "engine": "google",
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": "YOUR_SERPAPI_KEY"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get('organic_results', [])

# Function to send results to the Groq API for parsing
def send_to_groq(results, prompt):
    groq_api_url = 'YOUR_GROQ_API_ENDPOINT'
    headers = {'Authorization': 'Bearer YOUR_GROQ_API_KEY'}
    data = {
        'prompt': prompt,
        'results': results
    }
    response = requests.post(groq_api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Assuming the Groq API returns JSON data
    else:
        return {"error": "Failed to retrieve data from Groq API"}

# Function to write data back to Google Sheets
def write_to_google_sheet(sheet_url, data):
    credentials = Credentials.from_service_account_file('/absolute/path/to/your/service_account.json')
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url).sheet1
    for row in data:
        sheet.append_row(row)

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

    # Dynamic Query Input
    st.header("Dynamic Query Input")
    prompt_template = st.text_input("Define your custom prompt (use placeholders like {entity}):", "Get the email and address for {company}")

    if st.button("Generate Queries"):
        # Generate queries based on the selected main column
        queries = [prompt_template.format(entity=row[main_column]) for index, row in df.iterrows()]
        st.write("Generated Queries:")
        st.write(queries)

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

        # Google Sheets Output Integration
        if st.button("Write Extracted Data to Google Sheet"):
            sheet_url = st.text_input("Enter Google Sheet URL for writing data:")
            if sheet_url:
                try:
                    write_to_google_sheet(sheet_url, [[item['query'], item['extracted_data']] for item in extracted_info])
                    st.success("Data has been written to the Google Sheet.")
                except Exception as e:
                    st.error(f"Error writing to Google Sheet: {e}")

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
        prompt_template_google = st.text_input("Define your custom prompt for Google Sheet (use placeholders like {entity}):", "Get the email and address for {company}")
        
        if st.button("Generate Google Queries"):
            # Generate queries based on the selected main column from Google Sheet
            google_queries = [prompt_template_google.format(entity=row[main_column_google]) for index, row in df_google.iterrows()]
            st.write("Generated Google Queries:")
            st.write(google_queries)

            # Perform web searches for each Google query
            google_search_results = {}
            extracted_google_info = []  # To store extracted information

            for query in google_queries:
                google_search_results[query] = perform_web_search(query)

            # Display Google search results and send to Groq API
            for query, results in google_search_results.items():
                st.subheader(f"Results for: {query}")
                for result in results:
                    st.write(f"**Title:** {result.get('title')}")
                    st.write(f"**Link:** [Click Here]({result.get('link')})")
                    st.write(f"**Snippet:** {result.get('snippet')}")
                    st.write("---")

                # Send results to Groq API for parsing
                groq_response_google = send_to_groq(results, prompt_template_google.format(entity=query))
                st.write("Groq Response for Google Query:", groq_response_google)

                # Store the extracted information
                if "extracted_info" in groq_response_google:  # Assuming your Groq API responds with extracted information
                    extracted_google_info.append({
                        "query": query,
                        "extracted_data": groq_response_google["extracted_info"]
                    })

            # Display extracted information from Google search results
            st.header("Extracted Information from Google Search")
            if extracted_google_info:
                for item in extracted_google_info:
                    st.write(f"**Query:** {item['query']}")
                    st.write(f"**Extracted Data:** {item['extracted_data']}")
                    st.write("---")
                    
    except Exception as e:
        st.error(f"Error connecting to Google Sheet: {e}")
