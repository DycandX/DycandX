#!/usr/bin/env python3
import urllib.request
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(HERE, "..", "README.md")

def get_weather():
    url = "https://wttr.in/Semarang?format=%c+%t+%C"
    req = urllib.request.Request(url, headers={'User-Agent': 'curl'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            text = response.read().decode('utf-8').strip()
            # Clean up extra spaces
            text = re.sub(r'\s+', ' ', text)
            return text
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def update_readme(weather_text):
    if not os.path.exists(README_PATH):
        print(f"README.md not found at {README_PATH}")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- WEATHER_START -->.*?<!-- WEATHER_END -->"
    replacement = f"<!-- WEATHER_START -->\n<span>📍 <b>Semarang, ID:</b> {weather_text}</span>\n<!-- WEATHER_END -->"

    if not re.search(pattern, content, re.DOTALL):
        print("Weather placeholders not found in README.md")
        return

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated README.md with weather info.")

if __name__ == "__main__":
    weather = get_weather()
    if weather:
        update_readme(weather)
    else:
        print("Failed to update weather.")
