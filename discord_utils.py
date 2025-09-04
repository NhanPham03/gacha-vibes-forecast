import os
import requests

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