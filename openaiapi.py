import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
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