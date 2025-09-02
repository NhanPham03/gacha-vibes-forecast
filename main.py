# Import deps
import os
import time
import random
import requests
import warnings
from pytrends.request import TrendReq

# Local modules
from browsers import USER_AGENTS
from keywords import GACHA_KEYWORDS
from responses import generate_forecast, generate_error


# Load .env, duh
from dotenv import load_dotenv
load_dotenv()

# Ignore warnings from pytrends
warnings.filterwarnings(
  action="ignore",
  message=r".*Downcasting object dtype arrays on \.fillna.*",
  category=FutureWarning
)


# Load agents to avoid rate-limiting by Google
# Add proxies here, don't use free proxies
# Called by: get_trending_gacha_game()
def create_pytrends():
  user_agent = random.choice(USER_AGENTS)
  headers = {'User-Agent': user_agent}
  print(f"[LOG] Current pytrends session with User-Agent:\n     {user_agent}")
  return TrendReq(hl='en-US', tz=360, requests_args={'headers': headers})


# Get data for forecast
# Will be passed to generate_forecast()
def get_trending_gacha_games():
  print("[LOG] Fetching Google Trends data for gacha games...")

  # Shuffle keywords so won't look like a bot script
  keywords = GACHA_KEYWORDS[:]
  random.shuffle(keywords)

  # Keywords are sorted into chunks of 2-4 to randomize requests
  chunks = []
  i = 0
  while i < len(keywords):
    chunk_size = random.randint(2, 4)   # Upper limit 5
    chunk = keywords[i:i+chunk_size]
    chunks.append(chunk)
    i += chunk_size

  # Store fetched data
  combined_data = {}

  for chunk in chunks:
    print(f"[LOG] Fetching trends for chunk: {chunk}")

    RETRY_COUNT = 3
    
    for attempt in range(RETRY_COUNT):
      try:
        pytrends = create_pytrends()
        pytrends.build_payload(chunk, timeframe='now 7-d')    # Upper limit 5, grab data from "7 days ago"
        data = pytrends.interest_over_time()
        if data.empty:
          print(f"[WARN] No trend data returned for chunk {chunk}")  # LOG
          break

        for game in chunk:
          combined_data[game] = data[game].iloc[-1]

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
  print(f"[ OK] Completed fetching trends. Sorted scores:")
  for game, score in sorted_scores:
    print(f"     {game}: {score}")
  return sorted_scores


# Tunnel the message through Discord webhook
# And cut up Gemini responses into chunks for posting
def post_to_discord(message):
  print("[LOG] Posting message to Discord...")
  MAX_LENGTH = 2000
  chunks = []

  while len(message) > MAX_LENGTH:
    # Attempt to split at endlines
    for end in ['\n\n', '\n', '. ']:
      cutoff = message.rfind(end, 0, MAX_LENGTH)

      if cutoff != -1 or cutoff >= MAX_LENGTH * 0.5:
        break
    else:
      cutoff = MAX_LENGTH       # If all else fails, cut at max length
    
    # Cut & append
    chunk = message[:cutoff].rstrip()
    chunks.append(chunk)
    message = message[cutoff:].lstrip()

  # Append message remainder
  if message:
    chunks.append(message)

  # Start posting chunks
  webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
  for i, chunk in enumerate(chunks, 1):
    print(f"[LOG] Posting chunk {i}/{len(chunks)} to Discord (length: {len(chunk)})...")
    try:
      res = requests.post(webhook_url, json={"content": chunk}, timeout=10)
      res.raise_for_status()
    except requests.RequestException as e:
      print(f"[ERR] Failed to post chunk {i} to Discord: {e}")
  
  print("[ OK] Finished posting message to Discord.")


# Don't spam Google Trends if rate-limited
def check_google_access():
  print("[LOG] Checking Google Trends accessibility...")
  try:
    res = requests.get("https://trends.google.com/trends/", timeout=10)
    if "Sorry" in res.text or res.status_code == 429:
      print("[WARN] Google Trends is rate-limited or unavailable.")
      return False
    print("[ OK] Google Trends is accessible.")
    return True
  except Exception as e:
    print(f"[ERR] Exception when checking Google Trends access: {e}")
    return False


# Stop script if no env vars
def check_env():
  for var in ["GOOGLE_API_KEY", "DISCORD_WEBHOOK_URL"]:
    if not os.getenv(var):
      raise Exception(f"Missing {var}. Ending script...")
  print("[ OK] All environment variables are set!")


# The steps of the script:
# 1. Check environment variables
# 2. Check Google Trends for rate-limits
# 3. Fetch trends for gacha games
# 4. Generate forecast
# 5. Post to Discord
def main():
  check_env()

  print("[LOG] Starting Gacha Vibes Forecast...")
  if not check_google_access():
    error = generate_error("Google Trends is currently rate-limiting or unavailable. Forecast will resume once the connection clears up!")
    post_to_discord(error)
    return

  trends = get_trending_gacha_games()
  if not trends:
    error = generate_error("No trend data available today. No forecast for today!")
    post_to_discord(error)
    return

  forecast = generate_forecast(trends)
  post_to_discord(forecast)
  print("[ OK] Completed Gacha Vibes Forecast successfully!")


# ENSURE YOU'RE USING PROXIES, VPNS, ANYTHING
# GOD FORBID IF YOU GET YOUR IP MARKED AS BOTTING
if __name__ == "__main__":
  main()
