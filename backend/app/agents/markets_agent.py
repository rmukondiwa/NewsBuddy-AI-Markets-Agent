import yfinance as yf
import logging
from ..llm import get_llm_response
from .base_agent import BaseAgent


class MarketsAgent(BaseAgent):
    def __init__(self):
        self.system_msg = (
            """You are a helpful assistant called 'FinanceBro' that provides information about financial markets.
                Talk like a College Fraternity Brother who is super into stocks and wants to work on Wall Street.
                You will use the given stock data and user input, then provide a concise and engaging summary,
                your thoughts on the reasonings behind the stock movements, and any advice you might have.
                Keep it brief and to the point. Add a little humor.
                But be concise whilst providing valuable bullet points.
                Although you sound like a frat bro, you need to sound really friendly
                and almost like a knowledgeable fun big brother."""  # noqa E501
        )
        self.description_msg = """
            - If the user input contains keywords related to financial markets, stocks, investing. Or even an actual stock ticker return:
            {"type": "MARKETS", "answer": "<the stock ticker belonging to the stock from user input>"}
        """  # noqa E501

    def handle_request(self, ticker: str, userInput: str) -> str:
        """Fetch stock data and summarize with LLM"""
        if not ticker:
            return "❌ Error: No ticker symbol provided."

        if ticker:
            logging.info(f"🟢 Fetching stock data for ticker: {ticker}")
            stockData = self.getStockPrice(ticker)
            prompt = self.buildMarketPrompt(userInput, stockData)
            return get_llm_response(prompt, system_msg=self.system_msg)

        return get_llm_response(userInput, system_msg=self.system_msg)

    def description(self) -> str:
        return self.description_msg

    # --- helper functions ---
    def getStockPrice(self, ticker: str) -> str:
        """
        Fetch the latest stock price using yfinance library.
        Returns a dict with ticker, price, and change percentage.
        """
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="5d", interval="1d")

            logging.info(f"Retrieved stock history: {history}")
            if history.empty:
                logging.error(f"❌ No historical data found for ticker: {ticker}")  #noqa E501
                return {"error": f"No historical data found for ticker {ticker}."}  # noqa E501

            currentPrice = history["Close"].iloc[-1]
            if len(history) > 1:
                previousClose = history["Close"].iloc[-2]
            else:
                previousClose = currentPrice

            if previousClose:
                changePercent = ((currentPrice - previousClose) / previousClose) * 100  # noqa E501
            else:
                changePercent = 0

            logging.info(f"🟢 Stock {ticker}: Price={currentPrice}, Change%={changePercent}")  # noqa E501
            return {
                "ticker": ticker,
                "TimePeriod": "5 days",
                "price": round(float(currentPrice), 2),
                "changePercent": round(float(changePercent), 2),
            }
        except Exception as e:
            logging.error("❌ Exception, fetching stock price has encountered error", exc_info=True)  # noqa E501
            return {"error": str(e)}

    def buildMarketPrompt(self, userInput: str, stockData: dict) -> str:
        """Construct user input with the market data retrieved from API to send to GPT"""  # noqa E501
        if "error" in stockData:
            return f"❌ User asked: {userInput}\nError: {stockData['error']}"

        if "ticker" in stockData:  # stock
            ticker = stockData.get("ticker", "N/A")
            price = stockData.get("price", "N/A")
            change = stockData.get("changePercent", "N/A")

            return (
                f"User asked: {userInput}\n\n"
                f"Stock Data:\n"
                f"- Ticker: {ticker}\n"
                f"- Current Price: ${price}\n"
                f"- Daily Change: {change}%\n"
            )
        return f"⚠️ User asked: {userInput}\nNo relevant market data available."  # noqa E501
    # noqa W292