import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from youtube_utils import youtube_handler
from article_utils import article_handler
from file_utils import file_handler

def is_youtube_url(url):
    return 'youtube.com' in url

        
def get_response(user_prompt):
    return "Empty Response"

def main():
    st.set_page_config(
        page_title="MENTORIA",
        page_icon="robot.png",
        menu_items={},
    )

    st.image("robot.png", width=150)
    st.header("MENTORIA")

    with st.sidebar:
        st.header("Data Sources")
        url = st.text_input("URL")
        docs = st.file_uploader("Upload your docs here", accept_multiple_files=True)

        if st.button("GO"):
            with st.spinner("Processing . . ."):
                url = url.lower()
                if is_youtube_url(url):
                    youtube_handler(url)
                elif url:
                    article_handler(url)
                
                file_handler(docs)
                

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Welcome to MENTORIA, How can I help U?")
        ]

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