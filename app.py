import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from rag_config import get_vectorstore, get_conversation
from url_utils import url_handler
from file_utils import file_handler


# Activated when GO clicked.
def click_go():
    st.session_state.GO = True


def main():
    # Load Google API key.
    load_dotenv()
    gemini_api_key = os.environ["GOOGLE_API_KEY"]

    # Page Configuration.
    st.set_page_config(
        page_title="MENTORIA",
        page_icon="data\logo 2.png",
        menu_items={},
    )
    st.image("data\logo 2.png", width=250)

    # Initialize session_state variables.
    if "chunks" not in st.session_state:
        st.session_state.chunks = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Welcome to Mentoria, how can I help you?")
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
                # Get chunks of text.
                if url:
                    url = url.lower()
                    st.session_state.chunks.extend(url_handler(url))
                if len(docs) > 0:
                    st.session_state.chunks.extend(file_handler(docs))

                # Get vectorstore.
                st.session_state.vectorstore = get_vectorstore(st.session_state.chunks)

                # Get conversation.
                st.session_state.conversation = get_conversation(
                    st.session_state.vectorstore, gemini_api_key
                )

    # Activiate the chat only when the user put data sources and click GO.
    if not st.session_state.GO:
        st.info(body="You must enter data sources", icon="⚠️")
    else:
        user_prompt = st.chat_input("Enter your prompt here . . .")

        if user_prompt is not None and user_prompt != "":
            user_question = user_prompt
            response = st.session_state.conversation.invoke(user_question)
            st.session_state.chat_history.append(HumanMessage(content=user_prompt))
            st.session_state.chat_history.append(AIMessage(content=response))

        # Show all messages.
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI", avatar="data\logo 2.png"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)


if __name__ == "__main__":
    main()
