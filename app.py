import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import YoutubeLoader
from vectorstore_config import get_vectorstore
import youtube_utils as yu
from langchain.text_splitter import RecursiveCharacterTextSplitter
from url_utils import article_handler
from file_utils import file_handler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain




def get_conversation_chain(repo_id, vectorstore):
    memory = ConversationBufferMemory(return_messages=True)
    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 800}
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain


def get_response(user_prompt):
    response = st.session_state.conversation({"question": user_prompt})
    return response


# Activated when GO clicked.
def click_go():
    st.session_state.GO = True


def main():
    load_dotenv()
    repo_id = os.environ["REPO_ID"]

    # Page Configuration.
    st.set_page_config(
        page_title="MENTORIA",
        page_icon="robot.png",
        menu_items={},
    )
    st.image("robot.png", width=150)
    st.markdown("# MENTORIA")

    # Initialize session_state variables.
    if "chunks" not in st.session_state:
        st.session_state.chunks = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Welcome to MENTORIA, How can I help U?")
        ]
    if "GO" not in st.session_state:
        st.session_state.GO = False
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    # Sidebar Components.
    with st.sidebar:
        with st.form(key="resources_form"):
            st.header("Data Sources")
            url = st.text_input("URL")
            docs = st.file_uploader("Upload your docs here", accept_multiple_files=True)
            st.form_submit_button("GO", on_click=click_go)

        if st.session_state.GO:
            with st.spinner("Processing . . ."):
                url = url.lower()
                if is_youtube_url(url):
                    st.write("is_youtube")
                    st.title("url")
                    st.write(url)
                    st.session_state.chunks.extend(yu.youtube_handler(url))
                    st.title("chunks")
                    st.write(st.session_state.chunks)
                    st.write("is_youtube_url ended.")
                elif url:
                    st.session_state.chunks.extend(article_handler(url))
                    st.write("ARTICLE_HELPER_DONE")  # for debugging.
                    # st.write(st.session_state.chunks)
                if len(docs) > 0:
                    st.session_state.chunks.extend(file_handler(docs))
                    st.write("FILE_HELPER_DONE")  # for debugging.
                    st.write(st.session_state.chunks)

                # Get vectorstore.
                if "conversation" not in st.session_state:
                    st.session_state.vectorstore = get_vectorstore(
                        st.session_state.chunks
                    )
                    st.session_state.conversation = get_conversation_chain(
                        repo_id, st.session_state.vectorstore
                    )

    # Activiate the chat only when the user put data sources.
    if not st.session_state.GO:
        st.info(body="You must enter data source", icon="⚠️")
    else:
        user_prompt = st.chat_input("Enter your prompt . . .")

        if user_prompt is not None and user_prompt != "":
            response = get_response(user_prompt)
            st.session_state.chat_history.append(HumanMessage(content=user_prompt))
            st.session_state.chat_history.append(AIMessage(content=response))

        # Show all messages.
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)


if __name__ == "__main__":
    main()
    # chunks = yu.youtube_handler('https://youtu.be/EzTxYQmU8OE?si=EXIZ-dm7QpuCvBdF')

    # for c in chunks:
    #     print(c)
    #     print('\n')
