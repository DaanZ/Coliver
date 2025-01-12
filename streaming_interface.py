import os

import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from airtable import create_qna, report_qna
from classify import classify_history
from streaming import llm_stream, process_stream

chat = ChatOpenAI(model="gpt-4o")



def streaming_interface(company_name: str, emoji: str, pages=None):
    st.set_page_config(
        page_title=f"{company_name}",
        page_icon=emoji,
        layout="wide"
    )
    #col1, col2 = st.columns([4,1])
    #with col1:
    st.image("data/coliver.png", width=250)
    #print(len(st.session_state.history.logs), st.session_state.initial_size)
    #if len(st.session_state.history.logs) > st.session_state.initial_size:
    #    with col2:
    #        if st.button("Report a wrong answer"):
    #            data = {"Question": st.session_state.history.logs[-2].content, "Answer": st.session_state.history.logs[-1].content}
    #            report_qna(data)

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
        assistant_text.markdown("⌂")
        # Stream response
        if pages:
            db = FAISS.from_documents(pages, OpenAIEmbeddings())
            for response in db.similarity_search(user_prompt, k=3):
                st.session_state.history.system(response.page_content)
            response_stream = llm_stream(st.session_state.history)
        else:
            response_stream = llm_stream(st.session_state.history)
        answers = process_stream(response_stream)
        chunk = ""
        for chunk in answers:
            assistant_text.markdown(chunk)  # Update progressively
        st.session_state.history.assistant(chunk)  # Save final message in history

        # Save to Airtable
        create_qna({"Question": user_prompt, "Answer": chunk})

        images = classify_history(user_prompt)
        if images:
            for image in images:
                if os.path.exists(image["path"]):
                    # Create two columns, display image in the left column (50% width)
                    col1, _ = st.columns([1, 2])  # 50% each column
                    with col1:
                        st.image(image["path"], caption=image["caption"], use_column_width=True)
                else:
                    st.warning("Image not found.")

    if len(st.session_state.history.logs) > st.session_state.initial_size:
        print("showing button")
        if st.button("Report answer"):
            print("reporting")
            report_qna({"Question": st.session_state.history.logs[-2]["content"],
                    "Answer": st.session_state.history.logs[-1]["content"]})
            #print("clicking report")
            #if st.session_state.report:
            #    st.session_state.report = None
            #else:
            #    st.session_state.report =

        #if st.session_state.report:
        #    reason = st.text_input("", placeholder="Report answer:")
        #    if st.button("Submit"):
        #        if reason:
        #            st.session_state.report["Reason"] = reason
        #        report_qna(st.session_state.report)
        #        st.session_state.report = None