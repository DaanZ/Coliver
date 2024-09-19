
import streamlit as st
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from history import History
from loader import history_pages, get_pages

company_name = "Coliver"
system_prompt = f"""You are a very kindly and Coliver assistant for {company_name}. You are
            currently having a conversation with a person. Answer the questions in a kind and friendly 
            with you being the expert for {company_name} to answer any questions about their coworking spaces."""


def query_path(query, history):
    pages = get_pages("website")
    embeddings = OpenAIEmbeddings()
    print(f"pages {len(pages)}")

    db = FAISS.from_documents(pages, embeddings)
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0.0, model_name="gpt-4o"),
        retriever=db.as_retriever(),
    )

    return chain.invoke({"question": query, "chat_history": history})["answer"]


def create_interface(emoji: str, history: History, optional: str = "", prompt=None):
    st.set_page_config(
        page_title=f"{company_name} GPT",
        page_icon=emoji,
        layout="wide"
    )

    st.title(f"{company_name} GPT")

    # check for messages in session and create if not exists
    if "history" not in st.session_state.keys():
        st.session_state.history = [SystemMessage(system_prompt)]
        st.session_state.history.append(AIMessage("Hello there, how can I help you? " + emoji + "\n"))

    # Display all messages
    for message in st.session_state.history:
        print(message)
        if isinstance(message, SystemMessage):
            continue
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

    user_prompt = st.chat_input()

    if user_prompt is not None:
        st.session_state.history.append(HumanMessage(user_prompt))
        with st.chat_message("user"):
            st.write(user_prompt)

    if not isinstance(st.session_state.history[-1], AIMessage):
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                chat = query_path(user_prompt, st.session_state.history)
                st.write(chat)
        st.session_state.history.append(AIMessage(chat))


if __name__ == "__main__":
    history: History = history_pages(f"website")
    create_interface("🌴🏠", history)
