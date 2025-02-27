import os

import rootpath
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pydantic import Field, BaseModel

from chatgpt import llm_strict
from history import History

categories: list[str] = ["Sauna instructions", "Parking my vehicle", "Kiosk instructions", "Groceries / Fridge instructions", "Washing Machines", "Activities Materials", "First Aid Supplies", "None of the above"]

images = {"Sauna instructions": [{"path": os.path.join(rootpath.detect(), "images", "sauna_knobs.png"), "caption": "Sauna Knobs"}],
          "Parking my vehicle": [{"path": os.path.join(rootpath.detect(), "images", "parking_1.jpg"), "caption": "Parking Entrance"},
                                 {"path": os.path.join(rootpath.detect(), "images", "parking_2.jpg"), "caption": "Don't park in front of the houses."}],
          "Kiosk instructions": [{"path": os.path.join(rootpath.detect(), "images", "kiosk.jpg"), "caption": "Electrical socket for Kiosk"}],
          "Groceries / Fridge instructions": [{"path": os.path.join(rootpath.detect(), "images", "fridge.jpg"), "caption": "Use your own label to put your groceries in the fridge"},
                                 {"path": os.path.join(rootpath.detect(), "images", "cupboard.jpg"), "caption": "Or use the cupboards with your our label."}],
          "First Aid Supplies": [{"path": os.path.join(rootpath.detect(), "images", "first_aid.jpg"), "caption": "First aid kit located on top of the Laundry room"}],
          "Washing Machines": [{"path": os.path.join(rootpath.detect(), "images", "washing_machines.jpg"), "caption": "Washing Machines located outside please use your own detergent and your own products please"}],
          "Activities Materials": [{"path": os.path.join(rootpath.detect(), "images", "activities.jpg"), "caption": "You can borrow the activities in exchange for good care."}]
          }


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
