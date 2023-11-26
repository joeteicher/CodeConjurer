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
