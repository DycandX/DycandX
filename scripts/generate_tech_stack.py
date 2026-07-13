#!/usr/bin/env python3
"""
Generate a beautiful, interactive, and glowing tech stack SVG card.
Displays all skills categorized in a 3-column masonry grid matching the user's design.
"""
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "tech-stack.svg")

# Design Constants
BG = "#0d1117"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#ffffff"
CARD_BG = "#161b22"

# Columns Layout Configuration
PAD_X = 24
PAD_Y = 16
COL_W = 265
GAP_X = 16
GAP_Y = 16
TITLEBAR_H = 30

CATEGORIES = [
    # Column 0
    {
        "title": "PROGRAMMING LANGUAGES",
        "color": "#00f2fe",  # Cyan glow
        "skills": ["Python", "JavaScript", "TypeScript", "C/C++", "PHP", "Java", "SQL", "MicroPython"],
        "col": 0
    },
    {
        "title": "DATABASES & SYSTEMS ANALYSIS",
        "color": "#34d399",  # Turquoise
        "skills": ["MySQL (Oracle Certified)", "PostgreSQL", "Oracle", "MongoDB", "ERD/DFD Architecture"],
        "col": 0
    },
    {
        "title": "TOOLS, DEVOPS & DEPLOYMENT",
        "color": "#22d3ee",  # Teal Cyan
        "skills": ["Git", "GitHub", "Vercel", "Google Analytics", "Postman API", "VS Code", "Linux OS", "Miro", "Notion", "Supabase"],
        "col": 0
    },
    # Column 1
    {
        "title": "WEB & FRAMEWORK TECHNOLOGIES",
        "color": "#fb923c",  # Orange
        "skills": ["Next.js", "Laravel", "Flutter", "Node.js", "Tailwind CSS", "Bootstrap"],
        "col": 1
    },
    {
        "title": "AUTOMATION & CORE PROTOCOLS",
        "color": "#fbbf24",  # Amber/Yellow
        "skills": ["ESP32/Arduino Firmware", "MQTT Broker", "UDP Sockets", "I2S Digital Audio", "PWM Control", "FreeRTOS", "Robot 2wd"],
        "col": 1
    },
    # Column 2
    {
        "title": "DATA SCIENCE, AI & ANALYTICS",
        "color": "#a78bfa",  # Violet
        "skills": ["TensorFlow", "Keras", "OpenCV", "MediaPipe", "Natural Language Processing (NLP)", "Data Scraping"],
        "col": 2
    },
    {
        "title": "METHODOLOGIES & FRAMEWORKS",
        "color": "#cbd5e1",  # Slate/Muted Grey
        "skills": ["CRISP-DM (Data Mining)", "SDLC (Waterfall / Agile Methodologies)"],
        "col": 2
    }
]

def layout_badges(skills, max_w):
    """
    Greedy layout badges into rows.
    """
    rows = [[]]
    current_w = 0
    
    for skill in skills:
        # Bracket text: "[ Python ]"
        display_text = f"[ {skill} ]"
        # Estimate width using monospaced font width (~5.8px per char) + padding (12px)
        badge_w = len(display_text) * 5.8 + 12
        
        # If it doesn't fit the row, wrap to next row
        if current_w + badge_w > max_w and rows[-1]:
            rows.append([])
            current_w = 0
            
        rows[-1].append({
            "text": skill,
            "w": badge_w
        })
        current_w += badge_w + 8  # 8px gap between badges
        
    return rows

def generate_svg():
    # We will build columns of cards and calculate canvas height dynamically
    columns_data = {0: [], 1: [], 2: []}
    columns_y = {0: TITLEBAR_H + PAD_Y, 1: TITLEBAR_H + PAD_Y, 2: TITLEBAR_H + PAD_Y}
    
    svg_elements = []
    
    for cat in CATEGORIES:
        col_idx = cat["col"]
        skills = cat["skills"]
        color = cat["color"]
        title = cat["title"]
        
        # Badge area width is COL_W - 24 (12px padding left/right)
        max_badge_area_w = COL_W - 24
        badge_rows = layout_badges(skills, max_badge_area_w)
        
        # Calculate card height dynamically
        # h = 16(top) + 16(title) + 14(gap) + len(rows)*22 + (len(rows)-1)*8 + 16(bottom)
        # h = 54 + len(rows)*30
        card_h = 54 + len(badge_rows) * 30
        
        card_x = PAD_X + col_idx * (COL_W + GAP_X)
        card_y = columns_y[col_idx]
        
        # Create Card Group
        card_parts = [
            f'<g class="card-group" style="--accent: {color};">',
            # Card Base
            f'  <rect class="card-bg" x="{card_x}" y="{card_y}" width="{COL_W}" height="{card_h}" rx="6"/>',
            # Left accent border
            f'  <rect class="accent-bar" x="{card_x}" y="{card_y}" width="3" height="{card_h}" rx="1.5" fill="{color}"/>',
            # Card Header Title
            f'  <text class="card-title" x="{card_x + 16}" y="{card_y + 26}">&gt; {title}</text>'
        ]
        
        # Render Badges Row-by-Row
        start_badge_y = card_y + 46
        for row_idx, row in enumerate(badge_rows):
            badge_x = card_x + 12
            badge_y = start_badge_y + row_idx * 30
            
            for badge in row:
                text = badge["text"]
                w = badge["w"]
                
                card_parts.append(f'  <g class="b-group">')
                # Badge background
                card_parts.append(f'    <rect class="b-bg" x="{badge_x:.1f}" y="{badge_y:.1f}" width="{w-2:.1f}" height="22" rx="4"/>')
                # Badge text
                text_x = badge_x + (w - 2) / 2
                text_y = badge_y + 15
                card_parts.append(
                    f'    <text class="b-text" x="{text_x:.1f}" y="{text_y:.1f}" text-anchor="middle">'
                    f'<tspan class="bracket">[ </tspan>'
                    f'<tspan class="skill-name">{text}</tspan>'
                    f'<tspan class="bracket"> ]</tspan>'
                    f'</text>'
                )
                card_parts.append(f'  </g>')
                
                badge_x += w + 8
                
        card_parts.append('</g>')
        svg_elements.append("".join(card_parts))
        
        # Advance Y position for this column
        columns_y[col_idx] += card_h + GAP_Y

    # Total Canvas height is max of columns + extra padding
    max_y = max(columns_y.values())
    canvas_w = 875
    canvas_h = max_y - GAP_Y + PAD_Y + 4  # ~630px to 660px depending on layout

    css = f"""
    .card-bg {{
      fill: {CARD_BG};
      stroke: #21262d;
      stroke-width: 1;
      transition: all 0.3s cubic-bezier(.2,.8,.2,1);
    }}
    .card-group:hover .card-bg {{
      stroke: var(--accent);
      filter: drop-shadow(0px 4px 12px rgba(0, 0, 0, 0.25));
    }}
    .accent-bar {{
      transition: all 0.3s ease;
    }}
    .card-group:hover .accent-bar {{
      filter: drop-shadow(0px 0px 8px var(--accent));
    }}
    .card-title {{
      fill: var(--accent);
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.5px;
      transition: all 0.3s ease;
    }}
    .card-group:hover .card-title {{
      filter: drop-shadow(0px 0px 4px var(--accent));
    }}
    
    /* Badges */
    .b-bg {{
      fill: {BG};
      stroke: #21262d;
      stroke-width: 1;
      transition: all 0.2s ease;
    }}
    .b-group:hover .b-bg {{
      stroke: var(--accent);
      fill: #1c2735;
      filter: drop-shadow(0px 0px 4px rgba(34, 211, 238, 0.2));
    }}
    .b-text {{
      font-size: 10px;
      font-weight: 700;
      transition: all 0.2s ease;
    }}
    .bracket {{
      fill: {MUTED};
    }}
    .skill-name {{
      fill: #e6edf3;
    }}
    .b-group:hover .bracket {{
      fill: var(--accent);
    }}
    .b-group:hover .skill-name {{
      fill: {TEXT};
    }}
    """.strip()

    # Final SVG assembly
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        # Canvas Background
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="{BG}"/>',
        # Outer Border
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
    ]

    # Titlebar Dots
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD_X + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
        
    parts.append(f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">zulvikar@is-a.dev: ~/skills</text>')
    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
    
    # Add Cards
    parts.extend(svg_elements)
    
    parts.append("</svg>")
    
    with open(OUT_PATH, "w") as f:
        f.write("".join(parts))
    print(f"Successfully generated {OUT_PATH} (width: {canvas_w}, height: {canvas_h})")

if __name__ == "__main__":
    generate_svg()
