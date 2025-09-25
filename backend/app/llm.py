import os
from openai import OpenAI


MODEL_ID = os.getenv("MODEL_ID")
LLM_TOKEN = os.getenv("LLM_TOKEN")
LLM_API_URL = os.getenv("LLM_API_URL")

# Initialize OpenAI client with appropriate credentials
client = OpenAI(
    api_key=LLM_TOKEN,
    base_url=LLM_API_URL,
)

def get_llm_response(req: str, system_msg: str = "") -> str:
    """
    Chat using LLM proxy. Uses the Responses API.
    """
    resp = client.responses.create(
        model=MODEL_ID,
        instructions=system_msg,
        input=req,
        temperature=0.7,
    )

    try:
        return resp.output[0].content[0].text
    except Exception as e:
        return f"Error extracting reply: {e}"
