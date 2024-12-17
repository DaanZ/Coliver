import os

import rootpath
import streamlit

from history import History
from loader import history_pages
from streaming_interface import streaming_interface


def load_knowledge(folder: str):
    return history_pages(os.path.join(rootpath.detect(), folder))


if __name__ == "__main__":
    company_name = "Coliver"
    emoji = "🏡🍹🐠"

    if "history" not in streamlit.session_state:
        streamlit.session_state.history = load_knowledge("unify")
        streamlit.session_state.history.system("You are an assistant for Coliver to answer any and all questions people have about Coliver, do not recommend contacting the team of Coliver for more information.")
        streamlit.session_state.history.assistant("""Welcome, Coliver!👋  
        I’m here to help with house rules 📋, shared spaces 🛋️, and community life 🎉—just ask! 🌟""")

    # Main program logic (call this function when you want to start the thread)
    try:
        streaming_interface(company_name, emoji, interface="Coliver")
    except KeyboardInterrupt:
        print("Program interrupted.")

