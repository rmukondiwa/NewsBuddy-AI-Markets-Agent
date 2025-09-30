import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s") # Set logging level to INFO so that we can see the logs

MODEL_ID = os.getenv("MODEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in environment variables")

# Initialize OpenAI client with appropriate credentials
client = OpenAI(api_key=OPENAI_API_KEY)
logging.info("OpenAI client initialized successfully")

def get_llm_response(req: str, system_msg: str = "") -> str:
    """
    Chat using LLM proxy. Uses the Responses API.
    req: user Input string
    system_msg: system prompt for the LLM
    """

    try:
        logging.info(f"Sending request to model {MODEL_ID} with system message: {system_msg}")

        resp = client.responses.create(
            model=MODEL_ID,
            instructions=system_msg,
            input=[{"role": "user", "content": req}],
            temperature=0.7,
        )
        response = resp.output[0].content[0].text
        logging.info(" Received response from OPENAI rahh")
        return response
    except Exception as e:
        logging.error(f" X Error extracting response: {e}")
        return f"Error extracting reply: {e}"
