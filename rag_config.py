"""
    Module the configure our RAG framework with its needed configuration.
    
    @author  Mohamed Hassan
    @version 1.0
    @since   2024-3-29
"""

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from url_utils import article_handler, youtube_handler
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory
from langchain_community.llms import HuggingFaceHub
from langchain.chains import ConversationalRetrievalChain
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


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

# Return a chain that deals with a retriever to answer.
# Doesn't have any memory yet.
def get_conversation(vectorstore, google_key):
    prompt = hub.pull("rlm/rag-prompt")
    retriever = vectorstore.as_retriever()
    llm = GoogleGenerativeAI(model="models/gemini-pro", google_api_key=google_key)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


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
