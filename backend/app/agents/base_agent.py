"""
Base AI agent: all agents should be able to respond to these "public" methods.
"""
class BaseAgent:
    def handle_request(self, input_text: str) -> str:
        """
        Given some input_text return an LLM response
        """
        # by default, do nothing
        return ""

    def description(self) -> str:
        """
        Return text describing the criteria for choosing your agent
        in the form of a dictionary with fields "type" and "answer"
        """
        # by default, do nothing
        return ""
