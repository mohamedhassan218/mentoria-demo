"""
    Module contains functions that handle the work with URLs.
    
    @author  Mohamed Hassan
    @version 1.0
    @since   2024-3-29
"""

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re


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


def article_handler(url):
    """
    This function is used to grap the content of the article by webscraping then
    it splits it into chunks.

    @param url: a string representing the URL of the article.
    @return result: list of strings represents the content of the article.
    """
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


def is_youtube_url(url):
    if url is not None and url != "":
        regExp = re.compile(
            r"^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*"
        )
        match = regExp.match(url)
        return match and len(match.group(2)) == 11


def url_handler(url):
    """
    This function is used to choose which handler should be called with the passed URL.

    @param url: a string represents the resource URL.
    @return result: a list of strings represents chunks of the content of the passed URL.
    """
    if is_youtube_url(url):
        result = youtube_handler(url)
    else:
        result = article_handler(url)
    return result


if __name__ == "__main__":
    # Test url_handler()
    res = url_handler(
        "https://www.techtarget.com/searchenterpriseai/definition/AI-Artificial-Intelligence"
    )
    print(f"Length of chunks: {len(res)}")
    print(res)

    # Test article_handler()
    article_chunks = article_handler(
        "https://www.techtarget.com/searchenterpriseai/definition/AI-Artificial-Intelligence"
    )
    print(f"Length of chunks: {len(article_chunks)}")
    print(article_chunks)

    # Test youtube_handler()
    youtube_chunks = youtube_handler("https://youtu.be/EzTxYQmU8OE?si=EXIZ-dm7QpuCvBdF")
    print(f"Length of chunks: {len(youtube_chunks)}")
    print(youtube_chunks)
