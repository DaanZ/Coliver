import os

import rootpath

from history import History
from loader import history_pages
from streaming_interface import streaming_interface


def load_knowledge(folder: str):
    return history_pages(os.path.join(rootpath.detect(), folder))


if __name__ == "__main__":
    company_name = "Coliver Coliving"
    emoji = "🏡🍹🐠"

    # Main program logic (call this function when you want to start the thread)
    try:
        history: History = load_knowledge("coliving")
        print(len(history.logs))
        streaming_interface(company_name, emoji, history, interface="Coliving")
    except KeyboardInterrupt:
        print("Program interrupted.")

