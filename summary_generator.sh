#!/usr/bin/env bash
set -e

# Helper to curl with silent mode, timeout, and fallback to N/A on failure
curl_fallback() {
  local url="$1"
  shift
  curl --max-time 10 -s "$@" "$url" 2>/dev/null || echo "N/A"
}

# Weather for major cities
weather_ny=$(curl_fallback "wttr.in/New%20York?format=%l:+%c+%t+%h+%w")
weather_london=$(curl_fallback "wttr.in/London?format=%l:+%c+%t+%h+%w")
weather_dubai=$(curl_fallback "wttr.in/Dubai?format=%l:+%c+%t+%h+%w")
weather_tokyo=$(curl_fallback "wttr.in/Tokyo?format=%l:+%c+%t+%h+%w")
weather_sydney=$(curl_fallback "wttr.in/Sydney?format=%l:+%c+%t+%h+%w")

# Tech insights via Hacker News (top 5)
tech_insights=""
if command -v jq >/dev/null; then
  top_ids=$(curl --max-time 10 -s "https://hacker-news.firebaseio.com/v0/topstories.json" | jq -r '.[:5]' 2>/dev/null || echo "")
  if [ -n "$top_ids" ]; then
    for id in $top_ids; do
      item=$(curl --max-time 10 -s "https://hacker-news.firebaseio.com/v0/item/$id.json")
      title=$(echo "$item" | jq -r '.title' 2>/dev/null || echo "N/A")
      url=$(echo "$item" | jq -r '.url // empty' 2>/dev/null || echo "")
      tech_insights="$tech_insights- $title"
      if [ -n "$url" ]; then
        tech_insights="$tech_insights\n  $url"
      fi
      tech_insights="$tech_insights\n"
    done
  else
    tech_insights="Unable to fetch tech news at the moment."
  fi
else
  tech_insights="jq not available; unable to parse tech news."
fi

# Joke
joke=$(curl_fallback -H "Accept: text/plain" "https://icanhazdadjoke.com/")

# Prices: only use jq if available
if command -v jq >/dev/null; then
  btc_json=$(curl_fallback "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?range=1d&interval=1m")
  gold_json=$(curl_fallback "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=1m")
  rates_json=$(curl_fallback "https://api.exchangerate.host/latest?base=USD&symbols=AED")
  btc_usd=$(echo "$btc_json" | jq -r '.chart.result[0].meta.regularMarketPrice' 2>/dev/null || echo "N/A")
  gold_usd=$(echo "$gold_json" | jq -r '.chart.result[0].meta.regularMarketPrice' 2>/dev/null || echo "N/A")
  aed_rate=$(echo "$rates_json" | jq -r '.rates.AED' 2>/dev/null || echo "N/A")
else
  btc_usd="N/A (jq missing)"
  gold_usd="N/A (jq missing)"
  aed_rate="N/A (jq missing)"
fi

# Compute AED values if numbers
btc_aed="N/A"
gold_aed="N/A"
if command -v awk >/dev/null && [[ "$btc_usd" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [[ "$aed_rate" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
  btc_aed=$(awk "BEGIN {printf \"%.2f\", $btc_usd * $aed_rate}")
fi
if command -v awk >/dev/null && [[ "$gold_usd" =~ ^[0-9]+(\.[0-9]+)?$ ]] && [[ "$aed_rate" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
  gold_aed=$(awk "BEGIN {printf \"%.2f\", $gold_usd * $aed_rate}")
fi

# Print summary
echo "Good morning! Here's your daily world summary:"
echo ""
echo "🌍 Global Weather:"
echo "$weather_ny"
echo "$weather_london"
echo "$weather_dubai"
echo "$weather_tokyo"
echo "$weather_sydney"
echo ""
echo "🤖 Tech & AI Insights:"
echo "$tech_insights"
echo ""
echo "😄 Joke of the Day:"
echo "$joke"
echo ""
echo "💰 Prices (USD / AED):"
echo "Bitcoin: $btc_usd USD / $btc_aed AED"
echo "Gold: $gold_usd USD / $gold_aed AED"
echo ""
echo "— Astra 🤖"
