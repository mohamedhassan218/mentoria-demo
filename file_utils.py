"""
    Module contains functions that handle the work with different file types
    like doc or docx, pdf, and txt.
    
    @author  Mohamed Hassan
    @version 1.0
    @since   2024-3-29
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, TextLoader
import streamlit as st
from PyPDF2 import PdfReader


def pdf_handler(doc):
    """
    This function is used to grap the content of pdf file then split it into chunks.

    @param doc: a File Object representing the pdf file that we wanna to get its content.
    @return chunks: list of strings represents the content of the inserted pdf.
    """
    pdf_reader = PdfReader(doc)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    return chunks


def word_handler(doc):
    """
    This function is used to grap the content of doc or docx file then split it into chunks.

    @param doc: a File Object representing the Word file that we wanna to get its content.
    @return chunks: list of strings represents the content of the inserted Word File.
    """
    loader = Docx2txtLoader(doc)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(data)
    result = [chunk.page_content for chunk in chunks]
    return result


def text_handler(doc):
    """
    This function is used to grap the content of the text file then split it into chunks.

    @param doc: a File Object representing the text file that we wanna to get its content.
    @return chunks: list of strings represents the content of the inserted text file.
    """
    loader = TextLoader(doc)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(data)
    result = [chunk.page_content for chunk in chunks]
    return result


def file_handler(docs):
    """
    This function is used to choose which handler should be called with each doc
    according to the extension of each file.

    @param docs: a list of files that we wanna handle them.
    @return all_chunks: list of strings represents the content of the whole inserted files.
    """
    all_chunks = []
    for doc in docs:
        file_name = doc.name
        if file_name.endswith(".pdf"):
            st.write("pdf")
            chunks = pdf_handler(doc)
            all_chunks.extend(chunks)
        elif file_name.endswith(".doc") or file_name.endswith(".docx"):
            st.write("word")
            chunks = word_handler(doc)
            all_chunks.extend(chunks)
        elif file_name.endswith(".txt"):
            st.write("text")
            chunks = text_handler(doc)
            all_chunks.extend(chunks)
    return all_chunks


if __name__ == "__main__":
    # Test pdf_handler()
    pdf_chunks = pdf_handler(r"C:\Users\moham\Desktop\Papers\Octopus.pdf")
    print(f"Length of chunks is: {len(pdf_chunks)}")
    print(pdf_chunks)

    # # Test word_handler()
    word_chunks = word_handler(r"C:\Users\moham\Desktop\paper.docx")
    print(f"Length of chunks is: {len(word_chunks)}")
    print(word_chunks)

    # Test text_handler()
    text_chunks = text_handler(r"C:\Users\moham\Desktop\MENTORIA.txt")
    print(f"Length of chunks is: {len(text_chunks)}")
    print(text_chunks)
