import requests
from bs4 import BeautifulSoup

GAMES = [
  {
    "name": "Limbus Company",
    "links": {
      "official": "https://limbuscompany.com/",
      "steam": "https://store.steampowered.com/app/1973530/Limbus_Company/",
    },
    "news_func": "get_r1999_news",
  },
  {
    "name": "Wuthering Waves",
    "links": {
      "official": "https://wutheringwaves.kurogames.com/en/main/",
      "steam": "https://store.steampowered.com/app/3513350/Wuthering_Waves/",
    },
    "news_func": "get_wuwa_news",
  },
  {
    "name": "Goddess of Victory: NIKKE",
    "links": {
      "official": "https://nikke-en.com/",
      "steam": "",
    },
  },
  {
    "name": "Blue Archive",
    "links": {
      "official": "",
      "steam": "",
    },
  },
  {
    "name": "Reverse:1999",
    "links": {
      "official": "https://re1999.bluepoch.com/en/home/",
      "steam": "https://store.steampowered.com/app/3092660/Reverse_1999/",
    },
  },
]

def get_keywords():
  return [game["name"] for game in GAMES]

def get_r1999_news():
  url = "https://re1999.bluepoch.com/en/home/"

  try:
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.css.select("div.news-right-con-list")
    headlines = []

    for item in items:
      title = item.select_one(".news-right-con-list-left-title").string.strip()
      date = item.select_one(".news-right-con-list-left-time").string.strip()
      post_id = item.get("data-news", "").strip()
      if post_id:
        link = f"https://re1999.bluepoch.com/en/home/detail.html#newsId?{post_id}"
      else:
        link = url

      headlines.append(f"- [{date}] {title}\n  {link}")
    return "\n".join(headlines)
  except Exception as e:
    print(f"[ERR] Failed to fetch Reverse:1999 news: {e}")
    return None

def get_wuwa_news():
  url = "https://wutheringwaves.kurogames.com/en/main/"

  try:
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.css.select("div.article")
    headlines = []

    for article in articles:
      title = article.select_one(".text-row .text").string.strip()
      date = article.select_one(".time-row").string.strip()

      headlines.append(f"- [{date}] {title}\n  {url}")
    return "\n".join(headlines)
  except Exception as e:
    print(f"[ERR] Failed to fetch Wuthering Waves news: {e}")
    return None
