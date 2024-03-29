"""
    Module contains functions that handle the work with articles URLs.
    
    @author  Mohamed Hassan
    @version 1.0
    @since   2024-3-29
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader


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


if __name__ == "__main__":
    chunks = article_handler(
        "https://www.techtarget.com/searchenterpriseai/definition/AI-Artificial-Intelligence"
    )
    print(f"Length of chunks: {len(chunks)}")
    print(chunks)
