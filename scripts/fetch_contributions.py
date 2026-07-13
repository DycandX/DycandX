#!/usr/bin/env python3
import datetime
import json
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "DycandX")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

def fetch_year_contributions(year):
    url = f"https://github.com/users/{USERNAME}/contributions?from={year}-01-01&to={year}-12-31"
    print(f"Fetching contributions for {year}...", file=sys.stderr)
    resp = requests.get(url, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    
    h2_text = ""
    h2_el = soup.select_one("h2")
    if h2_el:
        h2_text = h2_el.get_text(strip=True)
    
    year_total = 0
    if h2_text:
        m = re.search(r"([\d,]+)\s+contribution", h2_text)
        if m:
            year_total = int(m.group(1).replace(",", ""))
            
    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        td_id = td.get("id")
        tooltip_el = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
        text = tooltip_el.get_text(strip=True) if tooltip_el else ""
        if re.search(r"no contributions", text, re.I):
            count = 0
        else:
            m = re.match(r"(\d+)", text)
            count = int(m.group(1)) if m else 0
        days.append({"date": date, "count": count})
    days.sort(key=lambda d: d["date"])
    
    calculated_total = sum(d["count"] for d in days)
    if year_total == 0:
        year_total = calculated_total
        
    return {
        "year": year,
        "total": year_total,
        "days": days
    }

if __name__ == "__main__":
    current_year = datetime.datetime.now().year
    # DycandX account was created in 2022
    start_year = 2022
    
    years_data = []
    lifetime_contributions = 0
    
    for y in range(start_year, current_year + 1):
        try:
            y_data = fetch_year_contributions(y)
            years_data.append(y_data)
            lifetime_contributions += y_data["total"]
        except Exception as e:
            print(f"Error fetching year {y}: {e}", file=sys.stderr)
            
    # Sort years in descending order (newest first)
    years_data.sort(key=lambda x: x["year"], reverse=True)
    
    data = {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lifetime_contributions": lifetime_contributions,
        "years": years_data
    }
    
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully wrote {OUT_PATH}: {lifetime_contributions} lifetime contributions across {len(years_data)} years.")
