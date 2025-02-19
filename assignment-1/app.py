import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set page config
st.set_page_config(page_title="Data Sweeper", layout='wide', page_icon=":bar_chart:")

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        font-family: Arial, sans-serif;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
        max-width: 900px;
        text-align: center;
        color: #4f8bf9;
    }
    .sidebar {
        background-color: #4f8bf9;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        color: white;
    }
    .stfileUploader {
        background-color: #f5f5f5;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        color: #4f8bf9;
        border: 2px dashed #4f8bf9;
        margin-bottom: 20px;
    }
    .stbutton {
        background-color: #4f8bf9;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stbutton:hover {
        background-color: #3a6bbf;
        color: white;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    .main {
        background-color: #f5f5f5;
    }
    h1 {
        color: #4f8bf9;
        font-size: 2.5rem;
    }
    h2 {
        color: #2c3e50;
        font-size: 1.8rem;
    }
    .stButton button {
        background-color: #4f8bf9;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #3a6bbf;
        color: white;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        background-color: #fff;
        padding: 15px;
        margin-top: 20px;
    }
    .stChart {
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .stDownloadButton button {
        background-color: #4f8bf9;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stDownloadButton button:hover {
        background-color: #3a6bbf;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("Data Sweeper")
st.write("Transform your file between CSV and Excel format with built-in data cleaning and visualization!")
st.write("Upload a CSV or Excel file to clean, analyze, and visualize your data.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Invalid file format. Please upload a file with {file_extension} extension.")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())
        
        st.subheader("Data Cleaning Options")
        
        if st.checkbox(f"Clean Data For {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates for {file.name}"):
                    original_count = len(df)
                    df.drop_duplicates(inplace=True)
                    st.write(f"Duplicates removed successfully. {original_count - len(df)} rows dropped.")
                    
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled with the mean of respective columns.")
            
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            chart_type = st.selectbox(f"Select Chart Type for {file.name}", ["Bar Chart", "Line Chart", "Area Chart"])
            
            if chart_type == "Bar Chart":
                st.bar_chart(df.select_dtypes(include='number').iloc[: , :2])
            elif chart_type == "Line Chart":
                st.line_chart(df.select_dtypes(include='number').iloc[: , :2])
            elif chart_type == "Area Chart":
                st.area_chart(df.select_dtypes(include='number').iloc[: , :2])
        
        # Convert the file (CSV to Excel)
        st.subheader("Convert the file")
        conversion_type = st.radio(f"Convert {file.name} to", ("CSV", "Excel"), key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
            buffer.seek(0)
            
            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed!")
