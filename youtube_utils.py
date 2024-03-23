import streamlit as st
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def youtube_handler(url: str):
    # st.write("youtube_utils entered")
    # st.title("url")
    # st.write(url)
    loader = YoutubeLoader.from_youtube_url(url)
    transcript = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(transcript)
    # loader = YoutubeLoader.from_youtube_url(url)
    # transcript = loader.load()
    # st.title("Transcript")
    # st.write(transcript)
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
    # chunks = text_splitter.split_documents(transcript)
    # st.title("Chunks")
    # st.write(chunks)
    # st.write("youtube_utils ended")
    # for c in chunks:
    #     print(c)
    # print("\n")
    result = [doc.page_content for doc in chunks]
    return result


# chunks = youtube_handler('https://youtu.be/EzTxYQmU8OE?si=EXIZ-dm7QpuCvBdF')

# for c in chunks:
#     print(c.page_content)
#     print('\n')

# # print(chunks)