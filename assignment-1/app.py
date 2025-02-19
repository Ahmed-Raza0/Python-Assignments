import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data sweeper", layout='wide')
st.title("Data sweeper")
st.write("Transform your file between CSV and Excel format with built-in data cleaning and visualization!")

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
        
    # Create some Visualizations
    st.subheader("Data Visualization")
    if st.checkbox(f"Show Visualizations for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[: , :2])

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
