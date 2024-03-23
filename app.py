import re
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from youtube_utils import youtube_handler
from article_utils import article_handler
from file_utils import file_handler


def is_youtube_url(url):
    youtube_pattern = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    regex = re.compile(youtube_pattern)
    match = regex.match(url)
    return bool(match)


def get_response(user_prompt):
    return "Empty Response"


def main():
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

    # Sidebar Components.
    with st.sidebar:
        st.header("Data Sources")
        url = st.text_input("URL")
        docs = st.file_uploader("Upload your docs here", accept_multiple_files=True)

        # 
        if st.button("GO"):
            with st.spinner("Processing . . ."):
                url = url.lower()
                if is_youtube_url(url):
                    st.session_state.chunks.extend(youtube_handler(url))
                    tmp = youtube_handler(url)
                    st.write("YOUTUBE_HELPER_DONE") # for debugging.
                    st.write(tmp)
                elif url:
                    st.session_state.chunks.extend(article_handler(url))
                    st.write("ARTICLE_HELPER_DONE") # for debugging.
                if len(docs) > 0:
                    st.session_state.chunks.extend(file_handler(docs))
                    st.write("FILE_HELPER_DONE") # for debugging.

                # See all chunks together. (for debugging)
                for ch in st.session_state.chunks:
                    st.write(ch)

    if url is None and docs is None:
        # user_prompt = st.chat_input("Enter your prompt . . .")
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
