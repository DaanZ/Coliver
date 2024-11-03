from chatgpt import llm_chat, openai_client
from history import History


def llm_stream(history, model_name: str = "gpt-4o-mini"):

    # Initialize the stream
    stream = openai_client.chat.completions.create(
        model=model_name,  # Adjust model as needed
        messages=history.logs,
        stream=True  # Enable streaming
    )

    return stream


def process_stream(stream, openai=True):
    assistant_message = ""
    # Stream chunks and concatenate them
    for chunk in stream:
        if openai:
            if chunk.choices[0].delta.content is not None:
                choice = chunk.choices[0]
                if choice.delta and choice.delta.content:
                    assistant_message += choice.delta.content
                yield assistant_message
        else:
            print(chunk)
            if chunk["answer"] is not None:
                assistant_message += chunk["answer"]
            yield assistant_message


def llm_summarize(text: str, instructions: str = "Summarize into one paragraph"):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    history = History()
    history.system(text)
    history.user(instructions)
    return llm_chat(history)
