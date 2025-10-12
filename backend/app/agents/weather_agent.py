import os
import requests
import logging
import json
from ..llm import get_llm_response
from .base_agent import BaseAgent

class WeatherAgent(BaseAgent):
    def __init__(self):
        self.api_key = os.getenv("API_NINJAS_KEY")
        if not self.api_key:
            raise ValueError("Missing API_NINJAS_KEY in environment variables")
        self.system_msg = (
            """You are a friendly, informative weather assistant called 'WeatherBro'.
            Talk like a College Fraternity Brother who is super into the weather and climate.
            You summarize current weather data for the given city, making your tone calm,
            optimistic, and concise. You will be given data in the metric system but convert it to imperial.
            Explain the temperature, humidity, wind, and general conditions
            in an engaging, natural way — as if you're chatting with a curious pledge.
            Include helpful advice such as clothing suggestions or activity recommendations."""  # noqa E501
        )
        self.description_msg = """
            - If the user input asks about weather, temperature, humidity, or forecast
              (e.g., "weather in Paris", "is it raining in New York?", "temperature in Durham"),
              return:
            {"type": "WEATHER", "answer": "[<latitude>, <longitude>]"}""" # noqa E501
        
    def handle_request(self, coords: list, user_input: str) -> str:
        """Gets weather data for given coordinates and summarize via LLM."""
        if not coords:
            return "❌ Error: No coordinates provided. Expected [latitude, longitude]."
        if isinstance(coords, str):
            try:
                coords = json.loads(coords)
            except json.JSONDecodeError:
                return f"❌ Error: Could not parse coordinates from input: {coords}"

        if not isinstance(coords, (list, tuple)) or len(coords) != 2:
            return "❌ Error: Invalid coordinates format. Expected [latitude, longitude]."

        lat, lon = coords
        logging.info(f"🟢 Fetching weather data for coordinates: ({lat}, {lon})")
        weather_data = self.get_weather_data(lat, lon)
        if not weather_data:
            return "❌ Error: Could not retrieve weather data."
        
        prompt = self.build_weather_prompt(user_input, lat, lon, weather_data)
        return get_llm_response(prompt, system_msg=self.system_msg)

    def description(self) -> str:
        return self.description_msg
    
    # --- helper functions ---
    def get_weather_data(self, lat: float, lon: float) -> dict:
        """Fetch weather data from API Ninjas using latitude and longitude."""
        try:
            url = f"https://api.api-ninjas.com/v1/weather?lat={lat}&lon={lon}&units=imperial"
            headers = {"X-Api-Key": self.api_key}
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                logging.error(f"❌ API Error ({response.status_code}): {response.text}")
                return {"error": f"API returned {response.status_code}: {response.text}"}

            data = response.json()
            logging.info(f"🌤️ Received weather data: {data}")
            return data
        except Exception as e:
            logging.error("❌ Exception while fetching weather data", exc_info=True)
            return {"error": str(e)}

    def build_weather_prompt(self, user_input: str, lat: float, lon: float, weather_data: dict) -> str:
        """Construct prompt containing weather data and user’s coordinates."""
        if "error" in weather_data:
            return f"❌ User asked: {user_input}\nError: {weather_data['error']}"

        temperature = weather_data.get("temp", "N/A")
        feels_like = weather_data.get("feels_like", "N/A")
        humidity = weather_data.get("humidity", "N/A")
        wind_speed = weather_data.get("wind_speed", "N/A")
        condition = weather_data.get("condition", "N/A")

        return (
            f"User asked: {user_input}\n\n"
            f"Weather Data at Coordinates ({lat}, {lon}):\n"
            f"- Temperature: {temperature}°C\n"
            f"- Feels Like: {feels_like}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind Speed: {wind_speed} m/s\n"
            f"- Condition: {condition}\n"
        )