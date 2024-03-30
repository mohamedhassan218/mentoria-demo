import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import YoutubeLoader
from vectorstore_config import get_vectorstore
from url_utils import url_handler
from langchain.text_splitter import RecursiveCharacterTextSplitter
from url_utils import article_handler
from file_utils import file_handler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from vectorstore_config import get_vectorstore


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
    # st.session_state.vectorstore = get_vectorstore(st.session_state.chunks)


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
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    # Sidebar Components.
    with st.sidebar:
        with st.form(key="resources_form"):
            st.header("Data Sources")
            url = st.text_input("URL")
            docs = st.file_uploader("Upload your docs here", accept_multiple_files=True)
            st.form_submit_button("GO", on_click=click_go)

        if st.session_state.GO:
            with st.spinner("Processing . . ."):
                if url:
                    url = url.lower()
                    st.session_state.chunks.extend(url_handler(url))
                if len(docs) > 0:
                    st.session_state.chunks.extend(file_handler(docs))
                    st.write(st.session_state.chunks)

                # Get vectorstore
                st.session_state.vectorstore, st.session_state.retriever = (
                    get_vectorstore(st.session_state.chunks)
                )

    # Activiate the chat only when the user put data sources.
    if not st.session_state.GO:
        st.info(body="You must enter data sources", icon="⚠️")
    else:
        user_prompt = st.chat_input("Enter your prompt . . .")

        if user_prompt is not None and user_prompt != "":
            # Write the documents with the high similarity with the user_prompt.
            response = st.session_state.vectorstore.similarity_search(user_prompt)
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


# Errors:
# '''
#     docx:         TypeError: isfile: path should be string, bytes, os.PathLike or integer, not UploadedFile
#     txt:          Error loading UploadedFile(file_id='ba9e9d08-14f4-4897-9e9d-10cba5569c39', name='Transformers.txt', type='text/plain', size=1562, _file_urls=file_id: "ba9e9d08-14f4-4897-9e9d-10cba5569c39" upload_url: "/_stcore/upload_file/ea638215-036a-4b03-9aa9-aa4dfe72c7f5/ba9e9d08-14f4-4897-9e9d-10cba5569c39" delete_url: "/_stcore/upload_file/ea638215-036a-4b03-9aa9-aa4dfe72c7f5/ba9e9d08-14f4-4897-9e9d-10cba5569c39" )
#     youtube_url:  Bad request: Value error, The inputs are invalid, at least one input is required: received `[]` in `parameters`
# '''
