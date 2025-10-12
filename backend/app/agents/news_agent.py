import os
import logging
import requests
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from .base_agent import BaseAgent
from .markets_agent import MarketsAgent


class NewsSentimentAgent(BaseAgent):
    def __init__(self):
        # --- API Setup ---
        self.api_key = os.getenv("GNEWS_API_KEY")
        if not self.api_key:
            logging.warning("⚠️ GNEWS_API_KEY not found in environment variables")

        # --- Integrations ---
        self.markets_agent = MarketsAgent()  # reuse existing market logic

        # --- LangChain setup ---
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=True)
        self.chain = ConversationChain(llm=self.llm, memory=self.memory, verbose=False)

        # --- Meta Info for GatewayAgent ---
        self.system_msg = (
            """You are 'NewsMan', an intelligent market sentiment analyst.
            You summarize how media sentiment and market movements relate for a company.
            Include:
            - General news sentiment (positive/neutral/negative)
            - Supporting headlines
            - Market movement summary (from stock data)
            - Your analysis of why sentiment matches or diverges from price action.
            Speak conversationally but analytically. And provide your sources."""
        )

        self.description_msg = """
            - If the user asks about market or media sentiment for a company or stock,
              e.g. "What’s the news sentiment for Tesla this week?",
              return:
              {"type": "NEWS", "answer": "<company or stock ticker>"}
        """

    # --- Handle Request ---
    def handle_request(self, company: str, user_input: str) -> str:
        if not company:
            return "❌ Error: No company provided."

        company = self.normalize_ticker(company)
        logging.info(f"📰 Fetching news + stock sentiment for {company}")

        # Step 1: Fetch recent news
        news_context = self.get_recent_news(company)
        logging.info(f"📰 News context preview: {news_context[:200]}")

        # Step 2: Fetch stock data
        stock_data = self.markets_agent.getStockPrice(company)

        # Step 3: Build combined prompt
        prompt = self.build_sentiment_prompt(user_input, company, news_context, stock_data)

        # Step 4: Run through LangChain
        result = self.chain.invoke({"input": prompt})
        logging.info(f"🧠 LangChain raw result: {result}")

        # Extract clean text (LangChain returns dict)
        if isinstance(result, dict):
            if "response" in result:
                result = result["response"]
            elif "text" in result:
                result = result["text"]
            elif "output_text" in result:
                result = result["output_text"]
            else:
                result = str(result)

        # Step 5: Return clean string
        final_response = f"📈 **Sentiment Summary for {company}**\n\n{str(result).strip()}"
        return final_response

    # --- Fetch GNews Data ---
    def get_recent_news(self, company: str) -> str:
        try:
            url = (
                f"https://gnews.io/api/v4/search?"
                f"q={company}&lang=en&country=us&max=5&token={self.api_key}"
            )
            logging.info(f"🌐 Fetching GNews for: {company}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            articles = data.get("articles", [])
            logging.info(f"📰 GNews returned {len(articles)} articles for {company}")

            # Fallback — try full company name if ticker returns nothing
            if not articles:
                mapping = {
                    "TSLA": "Tesla", "AAPL": "Apple", "MSFT": "Microsoft",
                    "GOOGL": "Google", "META": "Meta", "AMZN": "Amazon",
                    "NVDA": "Nvidia",
                }
                fallback = mapping.get(company.upper(), company)
                if fallback != company:
                    logging.info(f"🔁 Retrying GNews with fallback query: {fallback}")
                    url = (
                        f"https://gnews.io/api/v4/search?"
                        f"q={fallback}&lang=en&country=us&max=5&token={self.api_key}"
                    )
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    articles = data.get("articles", [])
                    logging.info(f"📰 Fallback returned {len(articles)} articles for {fallback}")

            if not articles:
                return f"No recent news found for {company}."

            # Format headlines nicely
            lines = []
            for a in articles[:5]:
                title = a.get("title", "Untitled")
                source = a.get("source", {}).get("name", "Unknown Source")
                date = a.get("publishedAt", "Unknown Date")[:10]
                url = a.get("url", "")
                lines.append(f"- {title} ({source}, {date})\n  {url}")

            return "\n".join(lines)

        except Exception as e:
            logging.error("❌ Error fetching GNews API articles", exc_info=True)
            return f"Error fetching news for {company}: {e}"

    # --- Build Combined Prompt for LLM ---
    def build_sentiment_prompt(self, user_input, company, news_context, stock_data):
        if "error" in stock_data:
            stock_summary = f"Error fetching stock data: {stock_data['error']}"
        else:
            ticker = stock_data.get("ticker", company.upper())
            price = stock_data.get("price", "N/A")
            change = stock_data.get("changePercent", "N/A")
            stock_summary = f"{ticker} current price: ${price}, change: {change}%."

        return (
            f"User asked: {user_input}\n\n"
            f"--- Recent News for {company} ---\n{news_context}\n\n"
            f"--- Market Context ---\n{stock_summary}\n\n"
            f"Now synthesize both to describe overall sentiment and reasoning."
        )

    # --- Normalize Company Names to Tickers ---
    def normalize_ticker(self, name: str) -> str:
        mapping = {
            "TESLA": "TSLA", "APPLE": "AAPL", "MICROSOFT": "MSFT",
            "GOOGLE": "GOOGL", "ALPHABET": "GOOGL",
            "META": "META", "FACEBOOK": "META",
            "NVIDIA": "NVDA", "AMAZON": "AMZN"
        }
        key = name.strip().upper()
        return mapping.get(key, key)