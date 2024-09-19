import glob
import json
import os

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

from history import History


def json_read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def load_knowledge_documents(path: str = "project.json"):
    texts = load_knowledge(path)
    pages = []
    for text in texts:
        pages.append(Document(page_content=text))

    return pages


def load_knowledge_logs(path: str = "project.json"):
    texts = load_knowledge(path)
    history = History()
    for text in texts:
        history.system(text)

    return history


def load_knowledge(path: str = "project.json"):
    data = json_read_file(path)

    texts = []
    keys = ["content", "segment", "product", "industry", "audience", "business"]
    meta_info = "Centerline is: "
    for key in keys:
        if key in data:
            meta_info += "\n- " + key + ": " + data[key]
    texts.append(meta_info)

    competitor_info = "Competitors are: "
    for competitor in data["competitors"]:
        competitor_info += "\n- " + competitor["name"]
    texts.append(competitor_info)

    for chapter in data["chapters"]:
        if "title" not in chapter:
            continue
        title = chapter["title"]
        for research in chapter["research"]:
            texts.append(title + " - " + research["section"] + ": " + research["report"])
        texts.append(title + ": " + chapter["introduction"])
        # TODO remove double named sections
        for section in chapter["sections"]:
            for s in section["sections"]:
                texts.append(title + " - " + section["title"] + " - " + s["section"] + ": " + s["paragraph"])
        texts.append(title + ": " + chapter["recommendation"])

    return texts


def history_pages(folder):
    paths = os.path.join(folder, "*.txt")
    history = History()
    for path in glob.glob(paths):
        loader = TextLoader(path, encoding="utf-8")
        text = loader.load()[0].page_content
        print(text)
        history.system(text)
    return history


def get_pages(folder):
    paths = os.path.join(folder, "*.txt")
    pages = []
    for path in glob.glob(paths):
        loader = TextLoader(path, encoding="utf-8")
        pages.extend(loader.load_and_split())
    return pages


if __name__ == "__main__":
    load_knowledge()
