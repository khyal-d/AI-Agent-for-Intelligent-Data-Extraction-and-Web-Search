import streamlit as st
import pandas as pd

# Streamlit app
st.title("Dashboard for File Upload")

# File Upload Section
st.header("Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.dataframe(df)

    # Select the main column
    main_column = st.selectbox("Select the main column:", df.columns)
    st.write(f"Selected Main Column: {main_column}")


def convert_to_direct_download_link(drive_link):
    """Convert Google Drive link to direct download link."""
    file_id = drive_link.split('/d/')[1].split('/')[0]
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Streamlit App
st.header("Sample Data from a Public Dataset")
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






# Optional: A Section to Display Sample Data from a Public Dataset
st.header("Sample Data from a Public Dataset")
sample_data_url = st.text_input("Enter URL of a CSV file or direct download link from drive (public):")

if sample_data_url:
    try:
        # Read the CSV from the provided URL
        df_sample = pd.read_csv(sample_data_url)
        st.write("Preview of Sample Data:")
        st.dataframe(df_sample)

        # Select the main column from the sample data
        main_column_sample = st.selectbox("Select the main column from Sample Data:", df_sample.columns)
        st.write(f"Selected Main Column from Sample Data: {main_column_sample}")
    except Exception as e:
        st.error(f"Error loading sample data: {e}")






# import streamlit as st
# import pandas as pd
# import gspread
# from google.oauth2.service_account import Credentials

# # Setup Google Sheets connection
# def google_sheet_connect(sheet_url):
#     # Load credentials from a service account JSON file
#     credentials = Credentials.from_service_account_file('path/to/your/service_account.json')
#     gc = gspread.authorize(credentials)
#     return gc.open_by_url(sheet_url).get_worksheet(0).get_all_records()

# # Streamlit app
# st.title("Dashboard for File Upload and Google Sheets Connection")

# # File Upload Section
# st.header("Upload CSV File")
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     st.write("Preview of Uploaded Data:")
#     st.dataframe(df)

#     # Select the main column
#     main_column = st.selectbox("Select the main column:", df.columns)
#     st.write(f"Selected Main Column: {main_column}")

# # Google Sheets Connection Section
# st.header("Connect to Google Sheet")
# sheet_url = st.text_input("Enter Google Sheet URL:")

# if sheet_url:
#     try:
#         google_data = google_sheet_connect(sheet_url)
#         df_google = pd.DataFrame(google_data)
#         st.write("Preview of Google Sheet Data:")
#         st.dataframe(df_google)

#         # Select the main column from Google Sheet
#         main_column_google = st.selectbox("Select the main column from Google Sheet:", df_google.columns)
#         st.write(f"Selected Main Column from Google Sheet: {main_column_google}")
#     except Exception as e:
#         st.error(f"Error connecting to Google Sheet: {e}")
