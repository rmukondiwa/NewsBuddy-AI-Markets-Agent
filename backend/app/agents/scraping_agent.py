import re
import requests
from bs4 import BeautifulSoup
from .base_agent import BaseAgent
from ..llm import get_llm_response

"""
AI agent: scrape a URL -> summarize with your LLM.

Requires: requests, beautifulsoup4
    pip install requests bs4
"""
class ScrapingAgent(BaseAgent):
    def __init__(self):
        self.system_msg = (
            "You are a helpful assistant that summarizes web pages. Provide a concise summary."
        )
        self.description_msg = """
            - If the user input contains a URL, return:
              {"type": "SCRAPE", "answer": "<the first URL from user input>"}
        """

    def handle_request(self, url: str) -> str:
        html = self.fetch_html(url)
        content = self.html_to_text(html)
        content = self.chunk(content)
        return get_llm_response(content, system_msg=self.system_msg)

    def description(self) -> str:
        return self.description_msg


    # -- helper functions ---
    def fetch_html(self, url: str, timeout: int = 15) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MiniAI-Agent/1.0; +https://example.com/bot)"
        }
        r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        r.raise_for_status()
        ctype = r.headers.get("Content-Type", "")
        if "text/html" not in ctype.lower():
            raise ValueError(f"Unsupported content type: {ctype}")
        return r.text

    def html_to_text(self, html: str) -> str:
        """Simple heuristics to find text within html tags."""
        soup = BeautifulSoup(html, "html.parser")

        # Remove non-content elements
        for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
            tag.decompose()

        # Heuristic: drop obvious chrome
        for tag in soup.find_all(["header", "footer", "nav", "form", "aside"]):
            # keep if it’s suspiciously long (might contain real content)
            if len(tag.get_text(" ", strip=True)) < 500:
                tag.decompose()

        # Keep title
        title = (soup.title.string.strip() if soup.title and soup.title.string else "").strip()

        # Main text
        text = soup.get_text(" ", strip=True)

        # Normalize whitespace
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n{2,}", "\n", text)

        if title and title not in text[:200]:
            text = f"{title}\n\n{text}"

        return text.strip()

    def chunk(self, text: str, max_chars: int = 6000) -> str:
        """Simple chunking to fit model token limits."""
        return text[:max_chars]
