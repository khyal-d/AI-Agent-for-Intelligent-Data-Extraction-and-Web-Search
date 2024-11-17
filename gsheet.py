import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import pandas as pd

st.title("Google Sheets Data with Streamlit")

# Upload the JSON credentials file
uploaded_file = st.file_uploader("Upload your Google Sheets JSON credentials", type="json")

if uploaded_file is not None:
    try:
        # Read the file as a string and load it as JSON
        string_data = uploaded_file.read().decode('utf-8')
        credentials_dict = json.loads(string_data)
        
        # Define the scope to read and manage sheets
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Create credentials object using the uploaded JSON file as dictionary
        credentials = Credentials.from_service_account_info(
            credentials_dict, scopes=scope
        )
        
        # Authorize the client
        client = gspread.authorize(credentials)
        
        # Input field for Google Sheet name or URL
        sheet_name_or_url = st.text_input("Enter Google Sheet Name or URL:")
        
        if sheet_name_or_url:
            try:
                # Open the Google Sheet using the name or URL
                if "https://docs.google.com" in sheet_name_or_url:
                    spreadsheet = client.open_by_url(sheet_name_or_url)
                else:
                    spreadsheet = client.open(sheet_name_or_url)
        
                # Select the first worksheet
                worksheet = spreadsheet.sheet1
        
                # Fetch all records from the sheet
                records = worksheet.get_all_records()
        
                # Convert records to DataFrame and display
                df = pd.DataFrame.from_records(records)
                st.write("Data from the Google Sheet:")
                st.dataframe(df)
        
            except gspread.exceptions.APIError as e:
                st.error(f"Google Sheets API Error: {e}")
                st.error("Ensure your Google Sheet is shared with the service account and the URL is correct.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    except json.JSONDecodeError:
        st.error("The uploaded file is not a valid JSON file. Please upload a correct credentials file.")


