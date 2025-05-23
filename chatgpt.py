import os
from openai import OpenAI

from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel

from history import History

openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
openai_embeddings = OpenAIEmbeddings()


def llm_question(query):
    logs = History()
    logs.user(query)
    answer = llm_chat(logs)
    return answer


def llm_chat(message_log: History, model_name: str = "gpt-4o-mini"):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai_client.chat.completions.create(
        model=model_name,  # The name of the OpenAI chatbot model to use
        messages=message_log.logs,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=1000,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.0,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


def llm_summarize(text: str, instructions: str = "Summarize into one paragraph"):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    history = History()
    history.system(text)
    history.user(instructions)
    return llm_chat(history)


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def llm_strict(history: History, model_name: str = "gpt-4o", base_model: type = CalendarEvent):
    completion = openai_client.beta.chat.completions.parse(
        model=model_name,
        messages=history.logs,
        response_format=base_model,
    )

    event = completion.choices[0].message.parsed
    return event
