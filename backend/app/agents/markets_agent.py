import re
import requests
import yfinance as yf
import logging
from ..llm import get_llm_response
from base_agent import BaseAgent

class MarketsAgent(BaseAgent):
    def __init__(self):
        self.system_msg = (
            "You are a helpful assistant called 'FinanceBro' that provides information about financial markets. Talk like a College Fraternity Brother who is super into stocks and wants to work on Wall Street. You will use the given stock data and user input, then provide a concise and engaging summary, your thoughts on the reasonings behind the stock movements, and any advice you might have. Keep it brief and to the point. Add a little humor. But be concise whilst providing valuable bullet points. Although you sound like a frat bro, you need to sound really friendly and almost like a knowledgeable fun big brother."
            
        )
        self.description_msg = """
            - If the user input contains keywords related to financial markets, return:
              {"type": "MARKETS", "answer": "<the relevant market information or URL>"}
        """

    def handle_request(self, query: str) -> str:
        # Here you can implement logic to fetch market data from an API or database
        # For simplicity, we'll just return a placeholder response
        return get_llm_response(query, system_msg=self.system_msg)

    def description(self) -> str:
        return self.description_msg
    
    #--- helper functions --->
    def extractTicker(self, user_input: str) -> str:
        """Extract stock ticker from user input using regex.
        Example: "What is the current price of AAPL?" -> "AAPL"
        """
        match = re.search(r"\b[A-Z]{1,5}\b", user_input.upper())
        
        if match:
            return match.group(0)
        else:
            logging.warning("No ticker symbol found in user input.")
            return None
        
    def getStockPrice(self, ticker: str) -> str:
        """
        Fetch the latest stock price using yfinance library.
        Returns a dict with ticker, price, and change percentage.
        """
        try:
            stock = yf.Ticker(ticker)
            if not stock.info or 'regularMarketPrice' not in stock.info:
                logging.error(f"No market data found for ticker: {ticker}")
                return f"Error: No market data found for ticker {ticker}."
            
            history = stock.history(period="1month", interval="1d")
            if history.empty:
                logging.error(f"No historical data found for ticker: {ticker}")
                return f"Error: No historical data found for ticker {ticker}."
            
            currentPrice = history["Close"].iloc[-1]
            if len(history) > 1:
                previousClose = history["Close"].iloc[-2]
            else:
                previousClose = currentPrice
            
            if previousClose:
                changePercent = ((currentPrice - previousClose) / previousClose) * 100 
            else:
                changePercent = 0
            
            return
            {
                "ticker": ticker,
                "TimePeriod": "1 month",
                "price": round(float(currentPrice), 2),
                "changePercent": round(float(changePercent), 2),
            }
        except Exception as e:
            logging.error("Exception, fetching stock price has encountered error")
            return {"error": str(e)}
        
        def formatMarketResponse(self, data: dict) -> str:
            """Turn a market data dictionary into a user-friendly string."""
            if "error" in data:
                return f"Error: {data['error']}"
            if "ticker" in data:
                return (f"The current price of {data['ticker']} over the last {data['TimePeriod']} is ${data['price']} "
                        f"with a change of {data['changePercent']}%.")
            return "No valid market data available."
