import os
import time
import random
import requests
from pytrends.request import TrendReq

from responses import generate_forecast, generate_error

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

USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
  "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
  "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
  "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:116.0) Gecko/20100101 Firefox/116.0",
]

def create_pytrends():
  user_agent = random.choice(USER_AGENTS)
  headers = {'User-Agent': user_agent}
  print(f"[LOG] Current pytrends session with User-Agent: {user_agent}")
  return TrendReq(hl='en-US', tz=360, requests_args={'headers': headers})

def get_trending_gacha_game():
  print("[LOG] Starting to fetch Google Trends data for gacha games...")

  # Shuffle & randomize keywords
  keywords = GACHA_KEYWORDS[:]
  random.shuffle(keywords)
  chunks = []

  i = 0
  while i < len(keywords):
    chunk_size = random.randint(2, 4)
    chunk = keywords[i:i+chunk_size]
    chunks.append(chunk)
    i += chunk_size

  combined_data = {}

  for chunk in chunks:
    print(f"[LOG] Fetching trends for chunk: {chunk}")
    RETRY_COUNT = 3
    for attempt in range(RETRY_COUNT):
      try:
        pytrends = create_pytrends()
        pytrends.build_payload(chunk, timeframe='now 4-d')
        data = pytrends.interest_over_time()
        if data.empty:
          print(f"[WARN] No trend data returned for chunk {chunk}")  # LOG
          break

        for game in chunk:
          combined_data[game] = data[game].iloc[-1]
          print(f"[LOG] {game}: {combined_data[game]}")

        sleep_time = random.randint(10, 15)
        print(f"[LOG] Sleeping for {sleep_time} seconds before next chunk...")
        time.sleep(sleep_time)
        break
      except Exception as e:
        print(f"[ERR] Attempt {attempt+1} failed for chunk {chunk}: {e}")
        if attempt < RETRY_COUNT - 1:
          wait_time = (2 ** attempt) * 5 + random.randint(0, 5)
          print(f"[LOG] Retrying in {wait_time} seconds...")
          time.sleep(wait_time)
        else:
          print(f"[ERR] Failed to fetch trends for chunk {chunk} after {RETRY_COUNT} attempts.")
  
  sorted_scores = sorted(combined_data.items(), key=lambda x: x[1], reverse=True)
  print(f"[OK] Completed fetching trends. Sorted scores: {sorted_scores}")
  return sorted_scores

def post_to_discord(message):
  webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
  if not webhook_url:
    raise Exception("Missing DISCORD_WEBHOOK_URL")
  
  print("[LOG] Starting to post message to Discord webhook...")
  MAX_LENGTH = 2000
  chunks = []

  while len(message) > MAX_LENGTH:
    # Look for preferred endings
    for end in ['\n\n', '\n', '. ']:
      cutoff = message.rfind(end, 0, MAX_LENGTH)

      if cutoff != -1 or cutoff >= MAX_LENGTH * 0.5:
        break
    else:
      cutoff = MAX_LENGTH       # FALLBACK
    
    chunk = message[:cutoff].rstrip()
    chunks.append(chunk)
    message = message[cutoff:].lstrip()

  if message:
    chunks.append(message)

  for i, chunk in enumerate(chunks, 1):
    print(f"[LOG] Posting chunk {i}/{len(chunks)} to Discord (length: {len(chunk)})...")
    try:
      res = requests.post(webhook_url, json={"content": chunk}, timeout=10)
      res.raise_for_status()
    except requests.RequestException as e:
      print(f"[ERR] Failed to post chunk {i} to Discord: {e}")
  print("[OK] Finished posting message to Discord.")

def check_google_access():
  print("[LOG] Checking Google Trends accessibility...")
  try:
    res = requests.get("https://trends.google.com/trends/", timeout=10)
    if "Sorry" in res.text or res.status_code == 429:
      print("[WARN] Google Trends is rate-limited or unavailable.")
      return False
    print("[OK] Google Trends is accessible.")
    return True
  except Exception as e:
    print(f"[ERR] Exception when checking Google Trends access: {e}")
    return False

def main():
  print("[LOG] Starting Gacha Vibes Forecast...")
  if not check_google_access():
    error = generate_error("Google Trends is currently rate-limiting or unavailable. Forecast will resume once the connection clears up!")
    post_to_discord(error)
    return

  trends = get_trending_gacha_game()
  if not trends:
    error = generate_error("No trend data available today. No forecast for today!")
    post_to_discord(error)
    return

  forecast = generate_forecast(trends)
  post_to_discord(forecast)
  print("[OK] Completed Gacha Vibes Forecast successfully.")

if __name__ == "__main__":
  main()
