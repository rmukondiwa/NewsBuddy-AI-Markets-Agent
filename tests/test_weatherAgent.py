import os
import sys
import pytest

# Ensure backend/ is on sys.path regardless of where pytest is run
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# noqa to ignore flake8 import order rules
from backend.app.agents.weather_agent import WeatherAgent  # noqa: E402


@pytest.fixture
def agent():
    return WeatherAgent()


def test_description_contains_expected_keywords(agent):
    """Ensure WeatherAgent description contains key phrases."""
    desc = agent.description()
    assert "weather" in desc.lower()
    assert "temperature" in desc.lower()
    assert "forecast" in desc.lower()
    assert "WEATHER" in desc


def test_build_weather_prompt_with_valid_data(agent):
    """WeatherAgent should correctly build a weather prompt with coordinates."""
    user_input = "What’s the weather like in New York?"
    lat, lon = 40.7128, -74.0060
    weather_data = {
        "temp": 20.0,
        "feels_like": 19.0,
        "humidity": 55,
        "wind_speed": 5.2,
        "condition": "Clear"
    }

    prompt = agent.build_weather_prompt(user_input, lat, lon, weather_data)
    assert "New York" in prompt
    assert "Temperature" in prompt
    assert "Humidity" in prompt
    assert f"({lat}, {lon})" in prompt


def test_build_weather_prompt_with_missing_data(agent):
    """WeatherAgent should handle missing fields gracefully."""
    user_input = "Give me the forecast."
    lat, lon = 35.0, 139.0
    weather_data = {"temp": 25.0}  # Only temperature available

    prompt = agent.build_weather_prompt(user_input, lat, lon, weather_data)
    assert "25.0" in prompt
    assert "Feels Like" in prompt
    assert "Humidity" in prompt
    assert "Condition" in prompt
