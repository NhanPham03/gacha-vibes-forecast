import os
import time
import requests
from pytrends.request import TrendReq
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

GACHA_KEYWORDS = [
  "Limbus Company",
  "Wuthering Waves",
  "NIKKE",
  "Blue Archive",
  "Girls' Frontline 2: Exilium",
  "Reverse:1999"
]

def get_trending_gacha_game():
  pytrends = TrendReq(hl='en-US', tz=360)
  chunks = [GACHA_KEYWORDS[i:i+5] for i in range(0, len(GACHA_KEYWORDS), 5)]

  combined_data = {}

  for chunk in chunks:
    try:
      pytrends.build_payload(chunk, timeframe='now 1-d')
      data = pytrends.interest_over_time()
      if not data.empty:
        for game in chunk:
          combined_data[game] = data[game].iloc[-1]
      time.sleep(5)
    except Exception as e:
      print(f"Failed to fetch trends for chunk {chunk}: {e}")
  
  sorted_scores = sorted(combined_data.items(), key=lambda x: x[1], reverse=True)
  return sorted_scores

def generate_forecast(trend_data):
  trend_lines = "\n".join([f"- {game}: {score}" for game, score in trend_data])
  prompt = f"""Here are today's Google Trends scores for popular gacha games:

{trend_lines}

YOU MUST FOLLOW THESE RULES WHEN GENERATING THE FORECAST:
- Write a short, witty 'Gacha Vibes Forecast' like a weather report.
- Highlight drama, hype, banner drops, or salty energy.
- Use bullet points, emojis, jokes, and character.
- Keep it under 500 words. Keep it concise but fun.
"""
  
  genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
  model = genai.GenerativeModel("gemini-2.5-flash")
  response = model.generate_content(prompt)
  return response.text.strip()

def post_to_discord(message):
  webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
  if not webhook_url:
    raise Exception("Missing DISCORD_WEBHOOK_URL")
  
  MAX_LENGTH = 2000
  chunks = []

  while len(message) > MAX_LENGTH:
    cutoff = max(
      message.rfind('\n\n', 0, MAX_LENGTH),
      message.rfind('\n', 0, MAX_LENGTH),
      message.rfind('. ', 0, MAX_LENGTH)
    )

    if cutoff == -1 or cutoff < MAX_LENGTH * 0.5:
      cutoff = MAX_LENGTH
    
    chunk = message[:cutoff].rstrip()
    chunks.append(chunk)
    message = message[cutoff:].lstrip()

  if message:
    chunks.append(message)

  for chunk in chunks:
    payload = {"content": chunk}
    res = requests.post(webhook_url, json=payload)
    res.raise_for_status()

def main():
  trends = get_trending_gacha_game()
  if not trends:
    post_to_discord("No trend data available today.")
    return
  forecast = generate_forecast(trends)
  post_to_discord(forecast)

if __name__ == "__main__":
  main()
