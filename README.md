# SmartSearch AI: Intelligent Data Extraction and Retrieval System

## Project Description
This project involves the development of an AI-driven application designed to facilitate intelligent data extraction and analysis using generative capabilities. The AI agent processes datasets and performs real-time web searches to extract specific information, structured and presented through an interactive dashboard.

## Key Features

1. **Dashboard for File Upload and Sheets Connection**: 
    - Users can upload CSV files or connect Google Sheets for automatic data input.
    - Offers a preview of the uploaded data and selection of the primary column for the search.

2. **Dynamic Query Input**:
    - Users define custom prompts with placeholders for personalized information retrieval.
    - Prompts dynamically adapt to each entity in the dataset.

3. **Automated Web Search and Retrieval**:
    - Executes web searches per user-defined parameters and accumulates search results efficiently.
    - Employs web scraping technologies like SerpAPI ensuring scalability and compliance with API limits.

4. **Information Parsing Using LLM**:
    - Integrates a Language Learning Model (LLM) to parse and extract required data fields from search results.
    - Ensures accurate and context-aware data extraction.

5. **User-friendly Data Presentation**:
    - Extracted information displayed in a tabular format for ease of analysis.
    - Downloadable in CSV format or updatable to Google Sheets.

## Technologies Used

- **Frontend**: Streamlit for dashboard UI.
- **Data Handling**: Pandas for CSV processing, Google Sheets API for Sheets integration.
- **Web Search**: SerpAPI.
- **AI Models**: LLM like GroqAPI.
- **Backend**: Python for process orchestration.

## Installation and Usage

1. Clone the repository, or just download steps.py(since this file has the entire code).
2. Import or Install these:
    import streamlit as st
    import pandas as pd
    from serpapi import GoogleSearch
    import gspread
    from google.oauth2.service_account import Credentials
    import requests  # For calling the Groq API
    import os
    from dotenv import load_dotenv

4. Run the application using `streamlit run steps.py`.
5. Use the provided csv files or personal csv files for input.
6. Access the dashboard via `http://localhost:port/` in your web browser.

## Future Enhancements
- Implement advanced error handling for API and data extraction processes.
- Explore additional interactive elements to expand data query capabilities.
- Continuous integration of additional APIs for improved data retrieval.

## Conclusion
This project exemplifies the integration of generative AI within data extraction and web search processes, emphasizing innovation in user applications and technical implementation.

## Project Status Update
I have not yet completed the "SmartSearch AI: Intelligent Data Extraction and Retrieval System" project due to ongoing college exams, which have required significant time and attention. However, I am committed to finishing the project before the year ends. 
Thank you for your understanding and patience, and do consider me for an interview.

## Special note for BREAKOUTAI and PAYTM
Hey there PAYTM and BREAKOUTAI, I wanted to share that while my project is still a work in progress due to juggling college exams, I'm really excited about the possibility of interning at Paytm or Breakout AI. I'm passionate about AI and data solutions, and I'm enthusiastic about the chance to learn and contribute to your teams. I'd love to have the opportunity to interview and discuss how I can bring value to your projects. 
Thanks a lot for considering me! 
