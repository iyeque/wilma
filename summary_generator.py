#!/usr/bin/env python3

import urllib.request
import json
import sys
import time

USER_AGENT = "Mozilla/5.0 (compatible; OpenClaw/1.0; +https://openclaw.ai)"
TIMEOUT = 10  # seconds

def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            return json.load(response)
    except Exception as e:
        return None

def fetch_text(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            return response.read().decode('utf-8').strip()
    except Exception as e:
        return None

# 1. Global Weather via Open-Meteo
cities = [
    ("New York", 40.7128, -74.0060),
    ("London", 51.5074, -0.1278),
    ("Dubai", 25.2048, 55.2708),
    ("Tokyo", 35.6762, 139.6503),
    ("Sydney", -33.8688, 151.2093)
]

weather_lines = []
for name, lat, lon in cities:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = fetch_json(url)
    if data and 'current_weather' in data:
        cw = data['current_weather']
        temp = cw.get('temperature', 'N/A')
        wind = cw.get('windspeed', 'N/A')
        code = cw.get('weathercode', 'N/A')
        weather_lines.append(f"{name}: {temp}°C, wind {wind} km/h, code {code}")
    else:
        weather_lines.append(f"{name}: N/A")

# 2. Tech & AI Insights via Hacker News
tech_insights = []
top_ids = []
hn_data = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json")
if hn_data and isinstance(hn_data, list):
    top_ids = hn_data[:5]

for id in top_ids:
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
    item = fetch_json(item_url)
    if item and 'title' in item:
        title = item['title']
        url = item.get('url', '')
        if url:
            tech_insights.append(f"- {title}\n  {url}")
        else:
            tech_insights.append(f"- {title}")
    else:
        tech_insights.append("- N/A")

if not tech_insights:
    tech_insights = ["Unable to fetch tech news."]

# 3. Joke of the Day
joke = fetch_text("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}) or "N/A"

# 4. Bitcoin price (USD & AED) via CoinGecko
btc_usd = btc_aed = "N/A"
btc_data = fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,aed")
if btc_data and 'bitcoin' in btc_data:
    btc_usd = btc_data['bitcoin'].get('usd', 'N/A')
    btc_aed = btc_data['bitcoin'].get('aed', 'N/A')

# 5. Gold price (USD) via Yahoo Finance + convert to AED using exchange rate
gold_usd = gold_aed = "N/A"
gold_url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=1m"
gold_headers = {'User-Agent': USER_AGENT}
gold_data = fetch_json(gold_url, headers=gold_headers)
if gold_data and 'chart' in gold_data and 'result' in gold_data['chart'] and len(gold_data['chart']['result']) > 0:
    try:
        gold_usd = gold_data['chart']['result'][0]['meta']['regularMarketPrice']
    except KeyError:
        gold_usd = "N/A"

# 6. Exchange rate USD -> AED
aed_rate = None
rate_data = fetch_json("https://api.exchangerate.host/latest?base=USD&symbols=AED")
if rate_data and 'rates' in rate_data and 'AED' in rate_data['rates']:
    aed_rate = float(rate_data['rates']['AED'])
    if isinstance(gold_usd, (int, float)):
        gold_aed = f"{gold_usd * aed_rate:.2f}"
    else:
        try:
            gold_usd_float = float(gold_usd)
            gold_aed = f"{gold_usd_float * aed_rate:.2f}"
        except:
            gold_aed = "N/A"
else:
    aed_rate = None

# Construct summary
summary = f"""Good morning! Here's your daily world summary:

🌍 Global Weather:
{chr(10).join(weather_lines)}

🤖 Tech & AI Insights:
{chr(10).join(tech_insights)}

😄 Joke of the Day:
{joke}

💰 Prices (USD / AED):
Bitcoin: {btc_usd} USD / {btc_aed} AED
Gold: {gold_usd} USD / {gold_aed} AED

— Astra 🤖"""

print(summary)
