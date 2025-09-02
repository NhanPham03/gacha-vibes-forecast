# gacha-vibes-forecast

![Python version](https://img.shields.io/badge/Python-3.12.4-green)
![LLM version](https://img.shields.io/badge/Gemini-Flash_2.5-green)

## License

- **Code**: Licensed under the [MIT License](./LICENSE)

## Project Structure

Inside of this Python project, you'll see the following folders and files:

```text
/
├── .github/worksflows/
│   └── forecast.yaml             # GitHub Actions workflow (Runs weekly)
│
├── browsers.py                   # User Agents browser config
├── keywords.py                   # Google Trends keywords
├── responses.py                  # Google Gemini API (Flash 2.5) prompts
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
| `GOOGLE_API_KEY`      | Use Gemini Flash 2.5 to generate forecasts |

## Commands

**MAKE SURE YOU'RE USING PROXIES, VPNS**
**REPEATED RUNS ON THE SAME IP WILL GET YOUR IP FLAGGED BY GOOGLE**

All commands are run from the root of the project, from a terminal:

| Command                           | Action                |
| :-------------------------------- | :-------------------- |
| `pip install -r requirements.txt` | Installs dependencies |
| `python main.py`                  | Runs the script       |
