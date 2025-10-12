import pytest
from backend.app.agents.news_agent import NewsSentimentAgent

@pytest.fixture
def agent():
    return NewsSentimentAgent()


def test_description_contains_expected_keywords(agent):
    """Verify that the description includes key instructions."""
    desc = agent.description_msg
    assert "NEWS" in desc
    assert "sentiment" in desc.lower()
    assert "company" in desc.lower()
    assert "stock" in desc.lower()


def test_normalize_ticker(agent):
    """Ticker normalization should map names to tickers correctly."""
    assert agent.normalize_ticker("Tesla") == "TSLA"
    assert agent.normalize_ticker("google") == "GOOGL"
    assert agent.normalize_ticker("Microsoft") == "MSFT"
    assert agent.normalize_ticker("UnknownCorp") == "UNKNOWNCORP"


def test_build_sentiment_prompt_with_valid_data(agent):
    """Ensure build_sentiment_prompt constructs a coherent analysis prompt."""
    user_input = "What's the market sentiment for Tesla?"
    company = "TSLA"
    news_context = "- Tesla beats earnings expectations (Forbes, 2025-10-10)"
    stock_data = {"ticker": "TSLA", "price": 250.50, "changePercent": 1.25}

    prompt = agent.build_sentiment_prompt(user_input, company, news_context, stock_data)
    assert "TSLA" in prompt
    assert "earnings" in prompt
    assert "price" in prompt
    assert "Now synthesize both" in prompt


def test_build_sentiment_prompt_with_error(agent):
    """Ensure that prompt gracefully handles stock data errors."""
    user_input = "Tell me about NVIDIA sentiment."
    company = "NVDA"
    news_context = "No recent news found for NVDA."
    stock_data = {"error": "Stock API unavailable"}

    prompt = agent.build_sentiment_prompt(user_input, company, news_context, stock_data)
    assert "Error fetching stock data" in prompt
    assert "Stock API unavailable" in prompt


def test_get_recent_news_with_mocked_response(monkeypatch, agent):
    """Mock GNews API call to ensure parsing logic works correctly."""
    fake_articles = {
        "articles": [
            {
                "title": "Tesla hits new AI milestone",
                "source": {"name": "Reuters"},
                "publishedAt": "2025-10-10T12:00:00Z",
                "url": "https://example.com/article"
            }
        ]
    }

    def mock_get(url):
        class MockResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self): return fake_articles
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    result = agent.get_recent_news("TSLA")
    assert "Tesla hits new AI milestone" in result
    assert "Reuters" in result
    assert "example.com" in result


def test_handle_request_with_mocked_dependencies(monkeypatch, agent):
    """Simulate full sentiment pipeline with mocked data."""
    # Mock markets agent to avoid API calls
    class MockMarketsAgent:
        def getStockPrice(self, company):
            return {"ticker": company, "price": 100.0, "changePercent": 2.0}

    agent.markets_agent = MockMarketsAgent()

    # Mock news fetch
    monkeypatch.setattr(agent, "get_recent_news", lambda c: "- Sample news headline (Forbes, 2025-10-10)")

    # Mock LangChain chain.invoke() to simulate an AI reply
    class MockChain:
        def invoke(self, inputs):
            return {"response": f"Simulated AI sentiment summary for {inputs['input'][:40]}..."}

    agent.chain = MockChain()

    response = agent.handle_request("Tesla", "What’s the sentiment on Tesla?")
    assert isinstance(response, str)
    assert "Sentiment Summary" in response
    assert "TSLA" in response or "Tesla" in response