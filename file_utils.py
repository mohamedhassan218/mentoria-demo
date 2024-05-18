"""
    Module contains functions that handle the work with different file types
    like doc or docx, pdf, and txt.
    
    @author  Mohamed Hassan
    @version 1.0
    @since   2024-3-29
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, TextLoader
from PyPDF2 import PdfReader
import os
from tempfile import NamedTemporaryFile


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
        chunk_size=700,
        chunk_overlap=250,
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
    bytes_data = doc.read()
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(bytes_data)
        data = Docx2txtLoader(tmp.name).load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=250,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(data)
        result = [chunk.page_content for chunk in chunks]
    os.remove(tmp.name)
    return result


def text_handler(doc):
    """
    This function is used to grap the content of the text file then split it into chunks.

    @param doc: a File Object representing the text file that we wanna to get its content.
    @return chunks: list of strings represents the content of the inserted text file.
    """
    text = ""
    for line in doc:
        text += str(line)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=250,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    return chunks


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
            chunks = pdf_handler(doc)
            all_chunks.extend(chunks)
        elif file_name.endswith(".doc") or file_name.endswith(".docx"):
            chunks = word_handler(doc)
            all_chunks.extend(chunks)
        elif file_name.endswith(".txt"):
            chunks = text_handler(doc)
            all_chunks.extend(chunks)
    return all_chunks
