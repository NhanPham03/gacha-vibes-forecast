import os
import google.generativeai as genai

# FORECAST
def generate_forecast(trend_data):
  google_api_key = os.getenv("GOOGLE_API_KEY")
  if not google_api_key:
    raise Exception("Missing GOOGLE_API_KEY")

  trend_lines = "\n".join([f"- {game}: {score}" for game, score in trend_data if score >= 10])
  prompt = f"""Here are today's Google Trends scores for popular gacha games:

{trend_lines}

! RESPONSE LAYOUT:
Gache Vibes Forecast: [Overall vibes for the day]
[Intro]

---

[Forecast by game]

---

[Outro]

! RESPONSE PATTERN FOR EACH GAME ("Forecast by game" section):
## [Game title] ([Score]) - [Vibes of the day (Specific game)]
- **[Event, banner, or character, anything content-related in caps, each line will be an event]**: [Vibes and details of event, community reaction, etc.]

! YOU MUST FOLLOW THESE RULES WHEN GENERATING THE FORECAST (DOs):
- The content will be posted to Discord, please keep it short and to the point.
- Write a witty 'Gacha Vibes Forecast' like a weather report.
- Highlight drama, hype, banner drops, or salty energy.
- Use bullet points, emojis, jokes, and character.
- Avoid too much brainrot terms, and spoilers.
- Add details where necessary (e.g. specific banners, characters, content).

! YOU MUST AVOID (DON'Ts):
- Don't keep the square brackets ("[]") in the layout, they are used to indicate a section.
- If trend data is missing or unavailable, do NOT generate a sample forecast. Just respond with an appropriate error or explanation.
"""
  genai.configure(api_key=google_api_key)
  model = genai.GenerativeModel("gemini-2.5-flash")
  response = model.generate_content(prompt)
  return response.text.strip()


# ERROR 429 OR NOT FORECAST
def generate_error(error_data):
  google_api_key = os.getenv("GOOGLE_API_KEY")
  if not google_api_key:
    raise Exception("Missing GOOGLE_API_KEY")
  
  prompt = f"""{error_data}

! YOU MUST FOLLOW THESE RULES WHEN GENERATING THE ERROR RESPONSE (DOs):
- The content will be posted to Discord, please keep it short and to the point.
- Write a witty 'Gacha Vibes Forecast' like a weather report, but error messages for readers.
- Use bullet points, emojis, jokes, and character.
- Avoid too much brainrot terms, and spoilers.

! YOU MUST AVOID (DON'Ts):
- Don't hallucinate or suggest anything that is not in the error message.
"""
  genai.configure(api_key=google_api_key)
  model = genai.GenerativeModel("gemini-2.5-flash")
  response = model.generate_content(prompt)
  return response.text.strip()