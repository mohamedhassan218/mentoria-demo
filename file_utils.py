import streamlit as st

def file_handler(docs):
    for doc in docs:
        if "pdf" in doc.name:
            st.write("pdf")
        elif "doc" in doc.name:
            st.write("word")
        elif "txt" in doc.name:
            st.write("text")