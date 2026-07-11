#!/usr/bin/env python3
import urllib.request
import json
import os
import re
import random

HERE = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(HERE, "..", "README.md")

FALLBACK_QUOTES = [
    {"q": "The only way to do great work is to love what you do.", "a": "Steve Jobs"},
    {"q": "Talk is cheap. Show me the code.", "a": "Linus Torvalds"},
    {"q": "Programs must be written for people to read, and only secondarily for machines to execute.", "a": "Harold Abelson"},
    {"q": "Simplicity is the soul of efficiency.", "a": "Austin Freeman"},
    {"q": "Make it work, make it right, make it fast.", "a": "Kent Beck"},
    {"q": "Strive not to be a success, but rather to be of value.", "a": "Albert Einstein"},
]

def get_quote():
    url = "https://zenquotes.io/api/random"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and isinstance(data, list) and len(data) > 0:
                return data[0]["q"], data[0]["a"]
    except Exception as e:
        print(f"Error fetching quote from ZenQuotes: {e}")
    
    # Fallback to random local quote
    print("Using fallback local quote.")
    fallback = random.choice(FALLBACK_QUOTES)
    return fallback["q"], fallback["a"]

def update_readme(quote, author):
    if not os.path.exists(README_PATH):
        print(f"README.md not found at {README_PATH}")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- QUOTE_START -->.*?<!-- QUOTE_END -->"
    
    # Render with nice formatting
    quote_html = f'<!-- QUOTE_START -->\n<p align="center"><i>"{quote}"</i> — <b>{author}</b></p>\n<!-- QUOTE_END -->'

    if not re.search(pattern, content, re.DOTALL):
        print("Quote placeholders not found in README.md")
        return

    new_content = re.sub(pattern, quote_html, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated README.md with new quote.")

if __name__ == "__main__":
    quote, author = get_quote()
    update_readme(quote, author)
