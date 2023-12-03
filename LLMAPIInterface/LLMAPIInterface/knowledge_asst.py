import openai
from openai import OpenAI
from llm_api import get_client

assistant = None
thread = None
client = None

def init():
    global assistant
    global thread
    global client
    client = get_client()
    asst_prompt = "You are a Knowledge Assistant specialized in software development.\n "
    asst_prompt += "Your role is to manage and organize a comprehensive knowledge base, "
    asst_prompt += "including code snippets, documentation, and contextual information about "
    asst_prompt += "various software tools and components.\n You are adept at retrieving relevant "
    asst_prompt += "information, understanding complex software systems, and providing clear, "
    asst_prompt += "concise explanations.\n Your expertise includes a wide range of programming "
    asst_prompt += "languages, software development methodologies, and current best practices "
    asst_prompt += "in the industry.\n When asked, synthesize information from the knowledge base "
    asst_prompt += "to answer questions, provide code examples, explain concepts, or offer guidance "
    asst_prompt += "on software development tasks. Always ensure your responses are accurate, "
    asst_prompt += "up-to-date, and aligned with the current context of the inquiry.\n"

    assistant = client.beta.assistants.create(
        instructions=asst_prompt,
        model="gpt-4-1106-preview",
        tools=[{"type":"retrieval"}]
    )
    thread = client.beta.threads.create()

def load_assistant():
    global assistant
    global thread
    global client
    client = get_client()
    assistant = client.beta.assistants.retrieve('asst_3b0d7b1c-3c3c-4a4b-9e8c-4b4a7c7d9a8c')
    thread = client.beta.threads.retrieve('thrd_3b0d7b1c-3c3c-4a4b-9e8c-4b4a7c7d9a8c')

import json
import os

def read_record(record_file):
    """
    Reads the record file to get the assistant's ID and the list of loaded files.

    Args:
        record_file: str, path to the record file.

    Returns:
        dict: A dictionary containing the assistant's ID and the list of loaded files.
    """
    if os.path.exists(record_file):
        with open(record_file, 'r') as file:
            return json.load(file)
    else:
        return {"assistant_id": None, "loaded_files": []}

def update_record(record_file, assistant_id, loaded_files):
    """
    Updates the record file with the assistant's ID and the list of loaded files.

    Args:
        record_file: str, path to the record file.
        assistant_id: str, the ID of the assistant.
        loaded_files: list, a list of loaded file names.
    """
    with open(record_file, 'w') as file:
        json.dump({"assistant_id": assistant_id, "loaded_files": loaded_files}, file)

def load_new_files(project_directory, record_file):
    """
    Loads new files from the project directory into the assistant.

    Args:
        project_directory: str, path to the project directory.
        record_file: str, path to the record file.
    """
    record = read_record(record_file)
    assistant_id = record["assistant_id"]
    loaded_files = record["loaded_files"]

    for file_name in os.listdir(project_directory):
        file_path = os.path.join(project_directory, file_name)
        if os.path.isfile(file_path) and file_name not in loaded_files:
            # Load the file into the assistant (assuming a function load_file exists)
            load_file(assistant_id, file_path)
            loaded_files.append(file_name)

    # Update the record with the new list of loaded files
    update_record(record_file, assistant_id, loaded_files)

def load_file(assistant_id, file_path):
    """
    Loads a file into the assistant.

    Args:
        assistant_id: str, the ID of the assistant.
        file_path: str, path to the file.
    """
    # Upload a file with an "assistants" purpose
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )
    # Load the file into the assistant
    assistant = client.beta.assistants.retrieve(assistant_id)
    assistant.file_ids.append(file.id)
    
