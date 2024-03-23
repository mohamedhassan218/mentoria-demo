from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import TextLoader
import streamlit as st
from PyPDF2 import PdfReader

# Work Successfully.
def pdf_handler(doc):
    pdf_reader = PdfReader(doc)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    # Each chunks is a text.
    for c in chunks:
        print(c)    
        print('\n')
    return chunks
    
def word_handler(doc):
    st.write('word_handler entered')
    st.write(doc)
    loader = UnstructuredWordDocumentLoader(doc) 
    data = loader.load()
    # data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    st.write(data)
    chunks = text_splitter.split_documents(data)
    
    st.write('word_handler ended')
    return chunks
    
def text_handler(doc):
    loader = TextLoader(doc, encoding='UTF-8')
    
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(data)
    return chunks


def file_handler(docs):
    all_chunks = []
    for doc in docs:
        if "pdf" in doc.name:
            st.write("pdf")
            chunks = pdf_handler(doc)
            all_chunks.extend(chunks)
        elif "doc" in doc.name:
            st.write("word")
            chunks = word_handler(doc)
            all_chunks.extend(chunks)
        elif "txt" in doc.name:
            st.write("text")
            chunks = text_handler(doc)
            all_chunks.extend(chunks)
    return all_chunks