import os

import rootpath
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pydantic import Field, BaseModel

from chatgpt import llm_strict
from history import History

categories: list[str] = ["Sauna instructions", "Parking my vehicle", "Kiosk instructions", "None of the above"]

images = {"Sauna instructions": [{"path": os.path.join(rootpath.detect(), "images", "sauna_knobs.png"), "caption": "Sauna Knobs"}],
          "Parking my vehicle": [{"path": os.path.join(rootpath.detect(), "images", "parking_1.jpg"), "caption": "Parking Entrance"},
                                 {"path": os.path.join(rootpath.detect(), "images", "parking_2.jpg"), "caption": "Don't park in front of the houses."}],
          "Kiosk instructions": [{"path": os.path.join(rootpath.detect(), "images", "kiosk.jpg"), "caption": "Electrical socket for Kiosk"}]}


def classify_conversation(user: str):
    pages = [Document(page_content=category) for category in categories]
    new_db = FAISS.from_documents(pages, OpenAIEmbeddings())
    docs_with_score = new_db.similarity_search_with_score(user)
    print(docs_with_score)


class CategoryQuantifying(BaseModel):
    category: str = Field(..., description="Which of the following categories does this comment mention something about, think of something similar to: " + ", ".join(categories))


def classify_history(user: str):
    history = History()
    history.user(user)
    answer: CategoryQuantifying = llm_strict(history, base_model=CategoryQuantifying)

    if answer.category in images:
        return images[answer.category]


if __name__ == "__main__":
    video_summary = "Where can I park my car?"
    history = History()

    print(classify_conversation(video_summary))
