import os
import requests

from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent

load_dotenv()

api_base = os.getenv("AZURE_API_BASE")
api_key = os.getenv("AZURE_API_KEY")

def get_weather(city: str) -> dict:
  """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
  response = requests.get(f"https://wttr.in/{city}?format=j1")
  data = response.json()
  if response.status_code != 200:
    return {"error": "Could not retrieve weather data."}
  return data

model = LiteLlm(
  model="azure_ai/gpt-4o-mini",
  api_base=api_base,
  api_key=api_key,
  api_version="2024-12-01-preview",
)

root_agent = Agent(
  name="weather_agent",
  model=model,
  description="Weather agent that provides current weather information.",
  instruction="""
  You are a weather agent. When prompted with a city name, you will respond with the current weather information for that city using the get_weather function.
  """,
  tools=[get_weather]
)
