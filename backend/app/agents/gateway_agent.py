import json
from ..llm import get_llm_response
from .chat_agent import ChatAgent
from .scraping_agent import ScrapingAgent
from .markets_agent import MarketsAgent


"""
Decision AI agent: given a natural language input, choose
appropriate agent to handle it or revert to basic Chat agent.

Add your new agents to its agents dictionary below and import them above.
The Chat agent is used as the default agent in case no others are appropriate.
"""
class GatewayAgent:

    
    def __init__(self):
        self.agents = {
            "SCRAPE" : ScrapingAgent(),
            # TODO: implement weather agent in class with data from
            #       https://api.weather.gov
            # TODO: implement your own agent(s)
            "MARKETS" : MarketsAgent(),
        }
        self.system_msg = """
            You are an intelligent assistant that decides between several options
            or just chat normally.
            Always return your output strictly as a JSON object with the keys
            `type` and `answer` based on the following criteria:
        """
        for a in self.agents.values():
            self.system_msg += a.description()


    def get_agent(self, user_input: str) -> dict:
        """Given some user_input, decide which agent to use"""
        response = get_llm_response(user_input, system_msg=self.system_msg)

        try:
            decision = json.loads(response)
            agent_type = decision.get("type", "").upper()
            answer = decision.get("answer", "")

            if agent_type not in self.agents.keys():
                # fallback
                return {"type": "CHAT",
                        "agent": ChatAgent(),
                        "answer": user_input}
            
            if agent_type == "MARKETS" and not answer:
                return {
                    "type": "CHAT",
                    "agent": ChatAgent(),
                    "answer": user_input
                }
            
            else:
                return {"type": agent_type,
                        "agent": self.agents[agent_type],
                        "answer": answer}

        except json.JSONDecodeError:
            # LLM response did not follow JSON format
            return {"type": "ERROR", "answer": response}
