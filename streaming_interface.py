import os

import rootpath
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel

from chatgpt import llm_strict
from history import History
from streaming import llm_stream, process_stream

chat = ChatOpenAI(model="gpt-4o")


class BooleanDecision(BaseModel):
    mentioned: bool


def check_decision_answer(message, answer):
    history = History()
    history.user(message)
    history.assistant(answer)
    history.user("Did the assistant say anything about the preheating of the sauna? Only return true or false:")
    decision = llm_strict(history, base_model=BooleanDecision)
    print(decision)
    return decision.mentioned


def streaming_interface(company_name: str, emoji: str, history: History, pages=None):
    st.set_page_config(
        page_title=f"{company_name}",
        page_icon=emoji,
        layout="wide"
    )
    st.title(f"{company_name}")

    # Initialize history if not already in session state
    if "history" not in st.session_state.keys():
        st.session_state.history = history

    # Display all previous messages
    for message in st.session_state.history.logs:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input()  # Input box for the user

    if user_prompt is not None:
        st.session_state.history.user(user_prompt)
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Placeholder for the assistant's reply
        assistant_message_placeholder = st.chat_message("assistant")
        assistant_text = assistant_message_placeholder.empty()

        # Stream response
        with st.spinner("Loading..."):
            if pages:
                print("langchain")
                db = FAISS.from_documents(pages, OpenAIEmbeddings())
                for response in db.similarity_search(user_prompt, k=3):
                    print("article: " + response.page_content)
                    st.session_state.history.system(response.page_content)
                response_stream = llm_stream(st.session_state.history)
            else:
                response_stream = llm_stream(st.session_state.history)
            answers = process_stream(response_stream)
            chunk = ""
            for chunk in answers:
                assistant_text.markdown(chunk)  # Update progressively
            st.session_state.history.assistant(chunk)  # Save final message in history

            if check_decision_answer(user_prompt, chunk):
                sauna_path = os.path.join(rootpath.detect(), "coliving", "images", "sauna_knobs.png")
                if os.path.exists(sauna_path):
                    # Create two columns, display image in the left column (50% width)
                    col1, _ = st.columns([1, 1])  # 50% each column
                    with col1:
                        st.image(sauna_path, caption="Sauna Knobs", use_column_width=True)
                else:
                    st.warning("Sauna knob image not found.")