"""
    Module the configure our vectorstore with its settings.
    
    @author  Mohamed Hassan
    @version 1.0
    @since   2024-3-29
"""

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from url_utils import article_handler, youtube_handler


def get_vectorstore(text_chunks):
    """
    This function is used to return a vectorstore object that we can use to
    query to our embedded data or pass it as a retrieval to the llm to use it
    during the RAG lifecycle.

    @param text_chunks: a list of strings that we extracted from different resources like
        files or URLs.
    @return vectorstore: a Vectorstore Object.
    """
    embeddings = HuggingFaceHubEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


# Test the vectorstore
if __name__ == "__main__":
    article_chunks = article_handler(
        "https://www.techtarget.com/searchenterpriseai/definition/AI-Artificial-Intelligence"
    )
    youtube_chunks = youtube_handler("https://youtu.be/EzTxYQmU8OE?si=EXIZ-dm7QpuCvBdF")
    vc = get_vectorstore(youtube_chunks)
    query = "What is React?"
    docs = vc.similarity_search(query)
    for doc in docs:
        print(doc)
        print()
