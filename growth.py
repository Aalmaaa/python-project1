import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title= "Data Sweeper", layout= 'wide')

#custom css
st.markdown(
    """
   <style>
   .stApp{
       background-color: black;
       color:white;
       }
       </style>
       """,
       unsafe_allow_html=True
)  

#title and decsription
st.title(" Datasweeper Sterling Integrator By Aalma Irteza")
st.write("Tram=nsform your files between CSV and Excel formats with built-in data cleaning and visualization Creating the project for quater 3!")
    
#file uploader
uploader_files = st.files_uploader("Upload your files (accepts CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=(True))
    
if uploader_files:
    for file in uploader_files:
               file_ext =os.path.splitext(file.name)[-1].lower()

    if file_ext == ".csv":
              df = pd.read_csv(file)
            
    elif file_ext == "xlsx":
              df = pd.read_excel(file)
            
    else:
              st.error(f"unsupproted file type: {file_ext}")

        #files details
              st.write("Preview the head of the Dataframe")
              st.dataframe("df.head"()) 

        #data cleaning options
              st.subheader(" Data Cleaning Options")
    if st.checkbox(f"Clean data for {file.name}"):
                 col1,col2 = st.columns(2)

    with col1:
             if st.button(f"Remove dupilcate from the file: {file.name}"):
              df.drop_duplicates(inplace=True)   
    st.write("Duplicates removed!")
            
    with col2:
             if st.button(f"Fil missing values for {file.name}"):
               numeric_cols = df.select_dtypes(include=['number']).colums
             df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].means())
             st.write(" Misssing values have been filled!")
             
             st.subheader("Select Columns to Keep")
             columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
             df = df[columns]

        #data visualtion
             st.subheader("Data Visualization")
             if st.checkbox(f"Shoe=w Visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion Options

             st.subheader("Conversion Options")
             conversion_type = st.radio(f"Convert {file.name} to:" , ["CVS" , "Excel"], key=file.name)
            
             if st.button(f"Convert{file.name}"):
                     buffer = BytesIO()
             if conversion_type == "CVS":
                 df.to.cvs(buffer, index=False)
                 file_name = file.name.replace(file_ext, ".cvs")
                 mime_type = "text/cvs"


             elif conversion_type == "Excel":
                     df.to.to_excel(buffer, index=False)
                     file_name = file.name.replace(file_ext, ".xlsx")
                     mime_type = "application/vnd.openxmlformats.officedocuments.spreadsheetml.sheet"
                     buffer.seek(0)  


             st.download_button(
               label=f"Download {file.name} as {conversion_type}",
               data=buffer,
               file_name=file_name,
               mime=mime_type

            )   
st.success("All files processed successfully!")

 
