#!/usr/bin/env python3
"""
Render data/contributions.json (produced by fetch_contributions.py) as a proper
GitHub-style contribution heatmap SVG showing two years (current and previous)
with a clean, modern, dark aesthetic, CSS reveal animations, a Less->More legend,
and the lifetime contribution count in the header.
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# GitHub-ish green ramp: empty -> brightest.
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 24
LEFT_LABEL_W = 32
TITLEBAR_H = 64
SEP_H = 1
SEC_HEADER_H = 24
MONTHS_ROW_H = 16
GRID_H = 7 * STEP # 105px
YEAR_GAP = 36

BG = "#0d1117"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#ffffff"
GREEN = "#39d353"

# reveal timing (one-shot sweep)
COL_T = 0.018   # per-column delay contribution (left -> right sweep)
ROW_T = 0.045   # per-row delay contribution (top -> bottom cascade)
CELL_DUR = 0.42


def level_for(count):
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def build_year_grid(year_days):
    if not year_days:
        return []
        
    first = datetime.date.fromisoformat(year_days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # Sunday=0
    
    grid = []
    col = [None] * lead_pad
    for d in year_days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    lifetime_contributions = data.get("lifetime_contributions", 0)
    years_list = data.get("years", [])
    
    # We display 2 years: current year and the previous year
    # Since the years are sorted descending, years_list[0] is current, years_list[1] is previous
    years_to_render = []
    if len(years_list) >= 1:
        years_to_render.append(years_list[0])
    if len(years_list) >= 2:
        years_to_render.append(years_list[1])
        
    n_cols = 53
    art_w = n_cols * STEP
    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD # 24 + 32 + 795 + 24 = 875px
    
    # Calculate height dynamically based on rendered years
    num_years = len(years_to_render)
    canvas_h = TITLEBAR_H + SEP_H + (num_years * (SEC_HEADER_H + MONTHS_ROW_H + GRID_H)) + ((num_years - 1) * YEAR_GAP) + (PAD * 2)
    
    css = f"""
@keyframes cell {{
  0%   {{ opacity: 0; transform: translateY(-6px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
.c {{ opacity: 0; animation: cell {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        # Background
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="{BG}"/>',
        # Outer Border
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
    ]
    
    # --- HEADER SECTION ---
    # Title on the left
    parts.append(f'<text x="{PAD}" y="32" fill="{TEXT}" font-size="16" font-weight="700">GitHub Contribution Heatmap</text>')
    # Subtitle with highlighted lifetime contributions
    parts.append(f'<text x="{PAD}" y="50" fill="{MUTED}" font-size="11" font-weight="700">'
                 f'LIFETIME: <tspan fill="{GREEN}">{lifetime_contributions:,}</tspan> CONTRIBUTIONS'
                 f'</text>')
                 
    # Legend on the right (top-aligned with the title)
    leg_x = canvas_w - PAD - 152
    parts.append(f'<text x="{leg_x}" y="31" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for color in PALETTE:
        parts.append(f'<rect x="{lx}" y="20" width="{CELL-1}" height="{CELL-1}" rx="2.2" fill="{color}"/>')
        lx += CELL + 1
    parts.append(f'<text x="{lx + 6}" y="31" fill="{MUTED}" font-size="10">More</text>')
    
    # Horizontal Separator
    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
    
    # --- RENDER EACH YEAR ---
    grid_left = PAD + LEFT_LABEL_W
    current_y = TITLEBAR_H + PAD
    
    for idx, year_data in enumerate(years_to_render):
        year = year_data["year"]
        total = year_data["total"]
        days = year_data["days"]
        
        # Build grid and limit columns to 53
        grid = build_year_grid(days)[:53]
        
        # Render Year Header (e.g., "533 contributions in 2026")
        parts.append(f'<text x="{PAD}" y="{current_y + 12}" fill="{TEXT}" font-size="13" font-weight="700">'
                     f'{total:,} contributions in {year}</text>')
        parts.append(f'<text x="{canvas_w - PAD}" y="{current_y + 12}" fill="{MUTED}" font-size="11" text-anchor="end">'
                     f'Jan - Dec</text>')
                     
        # Find month labels positions
        month_labels = []
        seen_months = set()
        for ci, column in enumerate(grid):
            for cell in column:
                if cell is None:
                    continue
                date = datetime.date.fromisoformat(cell[0])
                key = (date.year, date.month)
                if key not in seen_months and date.day <= 7:
                    seen_months.add(key)
                    month_labels.append((ci, date.strftime("%b")))
                break
                
        # Render Month Labels
        y_months = current_y + SEC_HEADER_H + 12
        for ci, label in month_labels:
            x = grid_left + ci * STEP
            parts.append(f'<text x="{x}" y="{y_months}" fill="{MUTED}" font-size="9">{label}</text>')
            
        # Render Weekdays Labels on the left
        grid_top = current_y + SEC_HEADER_H + MONTHS_ROW_H
        for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
            y = grid_top + wi * STEP + CELL * 0.78
            parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{wname}</text>')
            
        # Render Grid Cells
        for ci, column in enumerate(grid):
            gx = grid_left + ci * STEP
            for ri, cell in enumerate(column):
                if cell is None:
                    continue
                date_s, count, lvl = cell
                gy = grid_top + ri * STEP
                delay = ci * COL_T + ri * ROW_T
                plural = "s" if count != 1 else ""
                parts.append(
                    f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                    f'fill="{PALETTE[lvl]}" style="animation-delay:{delay:.3f}s">'
                    f'<title>{date_s}: {count} contribution{plural}</title></rect>'
                )
                
        # Advance Y position for the next year
        current_y += SEC_HEADER_H + MONTHS_ROW_H + GRID_H + YEAR_GAP
        
    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    if os.path.exists(IN_PATH):
        data = json.load(open(IN_PATH))
        svg = render(data)
        with open(OUT_PATH, "w") as f:
            f.write(svg)
        print(f"Successfully rendered {OUT_PATH} ({len(svg)} bytes) with multi-year layout.")
    else:
        print(f"Error: {IN_PATH} not found.", file=sys.stderr)
