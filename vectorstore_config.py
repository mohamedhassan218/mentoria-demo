from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from article_utils import article_handler
from youtube_utils import youtube_handler


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceHubEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


# chunks = article_handler("https://www.imdb.com/title/tt18075020/")

# vc = get_vectorstore(chunks)

# print(vc)