# gacha-vibes-forecast

[![Python version](https://img.shields.io/badge/Python-3.12.4-green)](https://www.python.org/downloads/release/python-3124/)
[![LLM version](https://img.shields.io/badge/Gemini-2.5_Flash-green)](https://deepmind.google/models/gemini/flash/)
[![License](https://img.shields.io/badge/License-MIT-blue)](./LICENSE)

## Project Structure

Inside of this Python project, you'll see the following folders and files:

```text
/
├── .github/worksflows/
│   └── forecast.yaml             # GitHub Actions workflow (Runs weekly, Thursday at 0:00 UTC)
│
├── browsers.py                   # User Agents browser config
├── keywords.py                   # Google Trends keywords
│
├── discord_utils.py              # Discord webhook functions
├── gemini_utils.py               # Google Gemini API (Flash 2.5) prompts
├── steam_utils.py                # Steam News API functions
│
├── main.py                       # Main script
│
└── requirements.txt
```

## Environment Variables

If you intend to run this locally, you'll need to create a `.env` file in the root of the project.
Else, set the GitHub Actions secrets with the same names.

Copy from `.env.example` and fill in the values:

| Variable              | Description                                |
| :-------------------- | :----------------------------------------- |
| `DISCORD_WEBHOOK_URL` | Required to send messages to Discord       |
| `GOOGLE_API_KEY`      | Use Gemini 2.5 Flash to generate forecasts |

## Commands

**MAKE SURE YOU'RE USING PROXIES, VPNS.**  
**REPEATED RUNS ON THE SAME IP WILL GET YOUR IP FLAGGED BY GOOGLE.**

All commands are run from the root of the project, from a terminal:

| Command                           | Action                |
| :-------------------------------- | :-------------------- |
| `pip install -r requirements.txt` | Installs dependencies |
| `python main.py`                  | Runs the script       |
