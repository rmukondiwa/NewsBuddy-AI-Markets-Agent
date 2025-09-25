from .base_agent import BaseAgent
from ..llm import get_llm_response


"""
Minimal AI agent: chat normally with your LLM.

No description given because it can handle anything.
"""
class ChatAgent(BaseAgent):
    def handle_request(self, message: str) -> str:
        return get_llm_response(message)
