from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import streamlit as st

# Work Successfully.
def article_handler(url):
    st.write("Article URL")
    loader = WebBaseLoader(url)
    doc = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(doc)
    result = [c.page_content for c in chunks]
    return result

# chunks = article_handler('https://www.imdb.com/title/tt18075020/')

# for c in chunks:
#     print(c.page_content)
#     print('\n')