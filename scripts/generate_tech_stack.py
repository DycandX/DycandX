#!/usr/bin/env python3
"""
Generate a beautiful, interactive, and glowing tech stack SVG card.
Displays all skills in a clean, horizontally-centered grid inside a single terminal box.
"""
import os
import json

DIR_NAME = os.path.dirname(__file__)
OUT_PATH = os.path.join(DIR_NAME, "..", "tech-stack.svg")
PATHS_JSON_PATH = os.path.join(DIR_NAME, "paths_data.json")

# Design Constants
BG = "#0d1117"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#ffffff"
CARD_BG = "#161b22"

# Layout Configuration
PAD_X = 32
PAD_Y = 24
TITLEBAR_H = 30
BADGE_H = 34
ROW_GAP = 12
BADGE_GAP = 12

# Fallback/Generic Icon (Code Tag `< >`)
FALLBACK_PATH = "M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"

# Skills List (Name, Brand Color)
SKILLS = [
    # Programming Languages
    ("Python", "#3776AB"),
    ("JavaScript", "#F7DF1E"),
    ("TypeScript", "#3178C6"),
    ("C/C++", "#00599C"),
    ("PHP", "#777BB4"),
    ("Java", "#F89820"),
    ("MicroPython", "#2599c9"),
    # Frameworks & Libraries
    ("Next.js", "#ffffff"),
    ("React", "#61DAFB"),
    ("Laravel", "#FF2D20"),
    ("Flutter", "#02569B"),
    ("Node.js", "#339933"),
    ("Tailwind CSS", "#38B2AC"),
    # AI & ML
    ("TensorFlow", "#FF6F00"),
    ("Keras", "#D00000"),
    ("OpenCV", "#5C3EE8"),
    ("MediaPipe", "#00f2fe"),
    ("Natural Language Processing (NLP)", "#a78bfa"),
    ("RAG", "#a78bfa"),
    # Databases & Systems
    ("PostgreSQL", "#4169E1"),
    ("MongoDB", "#47A248"),
    ("Supabase", "#3ECF8E"),
    ("Firebase", "#FFCA28"),
    # Embedded & IoT
    ("ESP32", "#E7352C"),
    ("Arduino", "#00979D"),
    ("MQTT", "#fbbf24"),
    # Tools & Platforms
    ("Git", "#F05032"),
    ("GitHub", "#ffffff"),
    ("Vercel", "#ffffff"),
    ("VS Code", "#007ACC"),
    ("Linux", "#FCC624"),
    ("Postman", "#FF6C37")
]

def load_paths():
    """
    Load paths from paths_data.json if exists.
    """
    if os.path.exists(PATHS_JSON_PATH):
        try:
            with open(PATHS_JSON_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def layout_badges(skills_data, paths_data, max_w):
    """
    Greedy layout badges into rows.
    """
    rows = [[]]
    current_w = 0
    
    for name, color in skills_data:
        # Check if we have an authentic icon path
        path = paths_data.get(name, FALLBACK_PATH)
        
        # Estimate width using monospaced font width (~6.0px per char) + padding
        # Badge layout: 12px padding left + 16px icon + 8px gap + text + 12px padding right
        # Total badge padding = 48px
        badge_w = len(name) * 6.0 + 48
        
        # If it doesn't fit the row, wrap to next row
        if current_w + badge_w > max_w and rows[-1]:
            rows.append([])
            current_w = 0
            
        rows[-1].append({
            "name": name,
            "color": color,
            "path": path,
            "w": badge_w
        })
        current_w += badge_w + BADGE_GAP
        
    return rows

def generate_svg():
    paths_data = load_paths()
    canvas_w = 875
    max_badge_area_w = canvas_w - 2 * PAD_X
    
    badge_rows = layout_badges(SKILLS, paths_data, max_badge_area_w)
    
    # Calculate canvas height dynamically
    # canvas_h = 30(titlebar) + 24(top padding) + len(rows)*34 + (len(rows)-1)*12 + 24(bottom padding)
    canvas_h = TITLEBAR_H + PAD_Y + (len(badge_rows) * BADGE_H) + ((len(badge_rows) - 1) * ROW_GAP) + PAD_Y
    
    css = f"""
    .b {{
      transition: all 0.3s cubic-bezier(.2,.8,.2,1);
      stroke: {FRAME};
      fill: #161b22;
      cursor: pointer;
    }}
    .b:hover {{
      stroke: var(--accent);
      fill: #1c2735;
      filter: drop-shadow(0px 0px 8px var(--accent));
    }}
    .icon {{
      fill: {MUTED};
      transition: all 0.3s ease;
    }}
    .b-group:hover .icon {{
      fill: var(--accent);
      filter: drop-shadow(0px 0px 4px var(--accent));
    }}
    .text {{
      fill: {MUTED};
      font-size: 11px;
      font-weight: 700;
      transition: all 0.3s ease;
    }}
    .b-group:hover .text {{
      fill: {TEXT};
    }}
    """
    
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        # Background
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="{BG}"/>',
        # Outer Border
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
    ]
    
    # Titlebar Dots
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD_X + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
        
    parts.append(f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">zulvikar@is-a.dev: ~/skills</text>')
    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
    
    # Render Centered Badges Row-by-Row
    start_badge_y = TITLEBAR_H + PAD_Y
    for row_idx, row in enumerate(badge_rows):
        # Calculate total width of this row to center it
        row_w = sum(b["w"] for b in row) + (len(row) - 1) * BADGE_GAP
        badge_x = (canvas_w - row_w) / 2
        badge_y = start_badge_y + row_idx * (BADGE_H + ROW_GAP)
        
        for badge in row:
            name = badge["name"]
            color = badge["color"]
            path = badge["path"]
            w = badge["w"]
            
            parts.append(f'<g class="b-group" style="--accent: {color};">')
            # Badge background rect
            parts.append(f'  <rect class="b" x="{badge_x:.1f}" y="{badge_y:.1f}" width="{w:.1f}" height="{BADGE_H}" rx="6"/>')
            
            # Icon (placed left-aligned inside the badge)
            icon_size = 16
            icon_x = badge_x + 12
            icon_y = badge_y + (BADGE_H - icon_size) / 2
            
            parts.append(f'  <svg x="{icon_x:.1f}" y="{icon_y:.1f}" width="{icon_size}" height="{icon_size}" viewBox="0 0 24 24">')
            parts.append(f'    <path class="icon" d="{path}"/>')
            parts.append(f'  </svg>')
            
            # Text (placed right of the icon)
            text_x = badge_x + 12 + icon_size + 8
            text_y = badge_y + BADGE_H / 2 + 4
            parts.append(f'  <text class="text" x="{text_x:.1f}" y="{text_y:.1f}">{name.replace("&", "&amp;")}</text>')
            parts.append(f'</g>')
            
            badge_x += w + BADGE_GAP
            
    parts.append("</svg>")
    
    with open(OUT_PATH, "w") as f:
        f.write("".join(parts))
    print(f"Successfully generated {OUT_PATH} (width: {canvas_w}, height: {canvas_h}) with {len(SKILLS)} skills.")

if __name__ == "__main__":
    generate_svg()
