import os
import sys
import pytest

# Ensure backend/ is on sys.path regardless of where pytest is run
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ignoring this flake8 security warning
# because we need to make project root correct
from backend.app.agents.markets_agent import MarketsAgent  # noqa: E402


@pytest.fixture
def agent():
    return MarketsAgent()


def test_description(agent):
    desc = agent.description()
    assert "MARKETS" in desc
    assert "stock" in desc.lower()
    assert "price" in desc.lower()
    # Verify that the NEWS distinction is clear
    assert "NEWS" in desc


def test_buildMarketPrompt_with_valid_data(agent):
    userInput = "What is the current status of AAPL?"
    stockData = {
        "ticker": "AAPL",
        "TimePeriod": "1 month",
        "price": 150.00,
        "changePercent": 2.5
    }

    prompt = agent.buildMarketPrompt(userInput, stockData)
    assert "AAPL" in prompt
    assert "150.0" in prompt
    assert "2.5%" in prompt


def test_buildMarketPrompt_with_missing_fields(agent):
    userInput = "Tell me about TSLA."
    stockData = {
        "ticker": "TSLA",
        # Missing TimePeriod
        "price": 700.00,
        # Missing changePercent
    }

    prompt = agent.buildMarketPrompt(userInput, stockData)
    assert "TSLA" in prompt
    assert "700.0" in prompt
    # It should not crash if optional fields are missing
    assert "N/A" in prompt or "changePercent" not in prompt
    # noqa W292