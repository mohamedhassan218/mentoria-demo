import streamlit as st
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def youtube_handler(url):
    st.write("Youtube Video")
    loader = YoutubeLoader.from_youtube_url(url)
    transcript = loader.load()
    st.write(transcript)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(transcript)
    st.write(chunks)
    return chunks