from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
import streamlit as st


def article_handler(url):
    st.write('Article URL')


def get_vectorstore_from_url(url):
    # Get the whole text from the website.
    loader = WebBaseLoader(url)
    doc = loader.load()

    # Split our text into chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(doc)

    # Create vectorstore from the chunks.
    embeddings = HuggingFaceHubEmbeddings()
    vector_store = Chroma.from_documents(chunks, embeddings)
    return vector_store