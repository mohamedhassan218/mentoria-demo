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
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import ConversationalRetrievalChain


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


def get_conversation(vectorstore, memory_llm_id, qa_llm_id, huggingface_token):
    memory_llm = HuggingFaceEndpoint(
        repo_id=memory_llm_id, max_length=128, temperature=0.7, token=huggingface_token
    )
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memory = ConversationSummaryMemory(
        llm=memory_llm, return_messages=True, memory_key="chat_history"
    )
    qa_llm = HuggingFaceEndpoint(
        repo_id=qa_llm_id, max_length=128, temperature=0.7, token=huggingface_token
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=qa_llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return chain


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
