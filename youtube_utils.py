"""
    Module contains functions that handle the work with youtube URLs.
    
    @author  Mohamed Hassan
    @version 1.0
    @since   2024-3-29
"""

from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def youtube_handler(url):
    """
    This function is used to grap the content of the Youtube video by catch the 
    transcript of the video then split it into chunks.

    @param url: a string representing the URL of the video.
    @return result: list of strings represents the chunks of the video transcript.
    """
    loader = YoutubeLoader.from_youtube_url(url)
    transcript = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(transcript)
    result = [doc.page_content for doc in chunks]
    return result


if __name__ == "__main__":
    chunks = youtube_handler("https://youtu.be/EzTxYQmU8OE?si=EXIZ-dm7QpuCvBdF")
    print(f"Length of chunks: {len(chunks)}")
    print(chunks)
