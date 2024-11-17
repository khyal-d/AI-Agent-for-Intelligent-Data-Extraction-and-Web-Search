import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Setup Google Sheets connection
def google_sheet_connect(sheet_url):
    # Load credentials from a service account JSON file
    credentials = Credentials.from_service_account_file('path/to/your/service_account.json')
    gc = gspread.authorize(credentials)
    return gc.open_by_url(sheet_url).get_worksheet(0).get_all_records()

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
    prompt_template = st.text_input("Define your custom prompt (use placeholders as {entity}):", f"Get me the email address of {{entity}} (selected column: {main_column})")
    # prompt_template = prompt_template.dropna(axis=1, how='all')
    if st.button("Generate Queries from CSV"):
        if df is not None and main_column in df.columns:
            queries = [prompt_template.format(entity=row[main_column]) for index, row in df.iterrows()]
            st.write("Generated Queries from CSV:")
            st.write(queries)
        else:
            st.warning("Please ensure you have selected a valid main column.")

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
        st.header("Dynamic Query Input for Google Sheet Data")
        prompt_template_google = st.text_input("Define your custom prompt for Google Sheet (use placeholders like {entity}):", "Get me the email address of {company}")
        
        if st.button("Generate Google Queries"):
            if df_google is not None and main_column_google in df_google.columns:
                google_queries = [prompt_template_google.format(entity=row[main_column_google]) for index, row in df_google.iterrows()]
                st.write("Generated Google Queries from Google Sheet:")
                st.write(google_queries)
            else:
                st.warning("Please ensure you have selected a valid main column.")

    except Exception as e:
        st.error(f"Error connecting to Google Sheet: {e}")











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

#     # Dynamic Query Input
#     st.header("Dynamic Query Input")
#     prompt_template = st.text_input("Define your custom prompt (use placeholders like {entity}):", "Get me the email address of {company}")
    
#     if st.button("Generate Queries"):
#         # Generate queries based on the selected main column
#         queries = [prompt_template.format(entity=row[main_column]) for index, row in df.iterrows()]
#         st.write("Generated Queries:")
#         st.write(queries)

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

#         # Dynamic Query Input for Google Sheet Data
#         prompt_template_google = st.text_input("Define your custom prompt for Google Sheet (use placeholders like {entity}):", "Get me the email address of {company}")
        
#         if st.button("Generate Google Queries"):
#             # Generate queries based on the selected main column from Google Sheet
#             google_queries = [prompt_template_google.format(entity=row[main_column_google]) for index, row in df_google.iterrows()]
#             st.write("Generated Google Queries:")
#             st.write(google_queries)

#     except Exception as e:
#         st.error(f"Error connecting to Google Sheet: {e}")


