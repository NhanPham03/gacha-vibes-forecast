import requests

def get_steam_news(steamapp_id, count=2, maxLength=500):
  url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"

  params = {
    "appid": steamapp_id,
    "count": count,
    "maxLength": maxLength
  }

  try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    news_items = response.json()["appnews"]["newsitems"]

    headlines = []
    for item in news_items:
      title = item.get("title", "")
      url = item.get("url", "")
      headlines.append(f"- {title}: {url}")
    return "\n".join(headlines)
  except Exception as e:
    return f"Couldn't fetch Steam news: {e}"