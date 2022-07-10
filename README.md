# Dhiraagu Usage Notifier

Telegram bot which scrapes data from dhiraagu portal

![screenshot](https://github.com/n4ff4h/dhiraagu-usage-notifier/blob/main/.github/screenshot.png?raw=true)

## Requirements

- [Python3](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
  ```
  curl -sSL https://install.python-poetry.org | python3 -
  ```

## Installation

Make sure to replace the contents of sample.env

```
git clone https://github.com/n4ff4h/dhiraagu-usage-notifier.git
cd dhiraagu-usage-notifier
poetry shell .
poetry install
cd dhiraagu_usage_notifier
mv sample.env .env
poetry run main.py
```
