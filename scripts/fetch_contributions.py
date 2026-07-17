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

def compute_current_streak(days):
    if not days:
        return 0, None, None
        
    # Get today's date in UTC
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    
    # Find the index of today in the days list
    idx = -1
    for i, d in enumerate(days):
        if d["date"] == today_str:
            idx = i
            break
            
    # If today is not in the list, fall back to the last day that is <= today_str
    if idx == -1:
        for i in range(len(days) - 1, -1, -1):
            if days[i]["date"] <= today_str:
                idx = i
                break
                
    if idx == -1:
        return 0, None, None
        
    # If today is 0, check if yesterday had contributions.
    # If yesterday is also 0, the current streak is 0.
    if days[idx]["count"] == 0:
        if idx > 0 and days[idx-1]["count"] == 0:
            return 0, None, None
        idx -= 1
        
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end

if __name__ == "__main__":
    current_year = datetime.datetime.now().year
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
            
    # Sort years ascending for chronological processing of streaks
    years_data.sort(key=lambda x: x["year"])
    
    all_days = []
    for y_data in years_data:
        all_days.extend(y_data["days"])
        
    # Calculate global stats
    cur_len, cur_start, cur_end = compute_current_streak(all_days)
    long_len, long_start, long_end = compute_longest_streak(all_days)
    best = max(all_days, key=lambda d: d["count"]) if all_days else {"date": None, "count": 0}
    
    # Sort years descending for JSON structure representation
    years_data.sort(key=lambda x: x["year"], reverse=True)
    
    # Optimize JSON size: only keep daily counts ('days') for the current and previous year
    for i, y_data in enumerate(years_data):
        if i >= 2:
            y_data.pop("days", None)
            
    data = {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lifetime_contributions": lifetime_contributions,
        "range": {"start": all_days[0]["date"] if all_days else None, "end": all_days[-1]["date"] if all_days else None},
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "years": years_data
    }
    
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully wrote {OUT_PATH}: {lifetime_contributions} lifetime contributions, "
          f"current streak {cur_len}, longest streak {long_len}.")
