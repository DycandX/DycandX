#!/usr/bin/env python3
"""
Generate a beautiful, interactive, and glowing tech stack SVG card.
Uses clean modern vector graphics and CSS hover glow effects.
"""
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "tech-stack.svg")

# Color Theme
BG = "#0d1117"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#ffffff"
CYAN = "#22d3ee"
GREEN = "#39d353"

# SVG Icons Paths (Simplified/Cleaned for render)
ICONS = {
    "Python": {
        "color": "#3776AB",
        "path": "M14.25.18a.25.25 0 0 0-.25.25v2.45c0 .06.05.11.11.11h3.78a2 2 0 0 1 2 2v1.5a.5.5 0 0 0 .5.5h2.46c.06 0 .11-.05.11-.11V4.28a4.1 4.1 0 0 0-4.1-4.1H14.25zM9.75 6.93a.5.5 0 0 0-.5.5v2.45a4.1 4.1 0 0 0 4.1 4.1h4.63a.25.25 0 0 0 .25-.25v-2.6c0-.06-.05-.11-.11-.11h-3.78a2 2 0 0 1-2-2v-1.5a.5.5 0 0 0-.5-.5H9.75z",
        "viewBox": "0 0 24 24"
    },
    "JavaScript": {
        "color": "#F7DF1E",
        "path": "M0 0h24v24H0V0zm20.066 17.2c-.53-.76-1.285-1.19-2.228-1.19-.944 0-1.54.498-1.54 1.205 0 .684.512 1.077 1.488 1.488 1.488.627 2.45 1.254 2.45 2.804 0 1.54-1.21 2.493-2.907 2.493-1.638 0-2.607-.798-3.177-1.924l1.638-1.012c.38.655.885.997 1.54.997.627 0 1.054-.313 1.054-.883 0-.612-.413-.912-1.34-1.312-1.368-.584-2.45-1.197-2.45-2.65 0-1.467 1.14-2.393 2.707-2.393 1.34 0 2.27.57 2.804 1.568l-1.467.812zm-8.032.556v7.218h-1.924V17.82h1.924z",
        "viewBox": "0 0 24 24"
    },
    "TypeScript": {
        "color": "#3178C6",
        "path": "M0 0h24v24H0V0zm20.066 17.2c-.53-.76-1.285-1.19-2.228-1.19-.944 0-1.54.498-1.54 1.205 0 .684.512 1.077 1.488 1.488 1.488.627 2.45 1.254 2.45 2.804 0 1.54-1.21 2.493-2.907 2.493-1.638 0-2.607-.798-3.177-1.924l1.638-1.012c.38.655.885.997 1.54.997.627 0 1.054-.313 1.054-.883 0-.612-.413-.912-1.34-1.312-1.368-.584-2.45-1.197-2.45-2.65 0-1.467 1.14-2.393 2.707-2.393 1.34 0 2.27.57 2.804 1.568l-1.467.812zm-8.032.556v7.218h-1.924V17.82h1.924z",
        "viewBox": "0 0 24 24"
    },
    "C++": {
        "color": "#00599C",
        "path": "M1.2 12c0-5.8 4.7-10.5 10.5-10.5 3.3 0 6.2 1.5 8.2 4l-2.6 2c-1.3-1.5-3.3-2.5-5.6-2.5-4.1 0-7.5 3.4-7.5 7.5s3.4 7.5 7.5 7.5c2.3 0 4.3-1 5.6-2.5l2.6 2c-2 2.5-4.9 4-8.2 4-5.8 0-10.5-4.7-10.5-10.5zm18.3-2h1.5v1.5H21v-1.5h1.5v-1.5H21v-1.5h-1.5v1.5h-1.5v1.5zm3.5 4.5h1.5V16h-1.5v-1.5H23v1.5h-1.5v1.5h1.5v1.5z",
        "viewBox": "0 0 24 24"
    },
    "PHP": {
        "color": "#777BB4",
        "path": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-12S17.52 2 12 2zm-1.8 13.9H8.7v-2.2H6.4v-1.5h2.3V9.8h1.5v2.4h2.2v1.5h-2.2v2.2z",
        "viewBox": "0 0 24 24"
    },
    "Java": {
        "color": "#007396",
        "path": "M2 10.5c0-.83.67-1.5 1.5-1.5h17c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5h-17c-.83 0-1.5-.67-1.5-1.5zm3-5C5 4.67 5.67 4 6.5 4h11c.83 0 1.5.67 1.5 1.5S18.33 7 17.5 7h-11C5.67 7 5 6.33 5 5.5zm-1 11c0-.83.67-1.5 1.5-1.5h13c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5h-13c-.83 0-1.5-.67-1.5-1.5z",
        "viewBox": "0 0 24 24"
    },
    "SQL": {
        "color": "#336791",
        "path": "M12 2C6.48 2 2 3.8 2 6v12c0 2.2 4.48 4 10 4s10-1.8 10-4V6c0-2.2-4.48-4-10-4zm0 2c4.82 0 8 1.41 8 2s-3.18 2-8 2-8-1.41-8-2 3.18-2 8-2zm-8 4.4c1.66.76 4.54 1.6 8 1.6s6.34-.84 8-1.6v2.2c0 .59-3.18 2-8 2s-8-1.41-8-2V8.4zm0 4.4c1.66.76 4.54 1.6 8 1.6s6.34-.84 8-1.6v2.2c0 .59-3.18 2-8 2s-8-1.41-8-2v-2.2z",
        "viewBox": "0 0 24 24"
    },
    "React": {
        "color": "#61DAFB",
        "path": "M22 12c0-1.1-.9-2-2-2h-3.5c-.5 0-1-.2-1.4-.6l-2.6-2.6c-.4-.4-.6-.9-.6-1.4V3.5c0-1.1-.9-2-2-2s-2 .9-2 2v3.5c0 .5-.2 1-.6 1.4L4.7 9.4c-.4.4-.9.6-1.4.6H2c-1.1 0-2 .9-2 2s.9 2 2 2h3.5c.5 0 1 .2 1.4.6l2.6 2.6c.4.4.6.9.6 1.4v3.5c0 1.1.9 2 2 2s2-.9 2-2v-3.5c0-.5.2-1 .6-1.4l2.6-2.6c.4-.4.9-.6 1.4-.6H20c1.1 0 2-.9 2-2z",
        "viewBox": "0 0 24 24"
    },
    "Node.js": {
        "color": "#339933",
        "path": "M12 2L2 7.7v11.5L12 25l10-5.8V7.7L12 2zm8 15.8l-8 4.6-8-4.6V8.9l8-4.6 8 4.6v8.9z",
        "viewBox": "0 0 24 24"
    },
    "Docker": {
        "color": "#2496ED",
        "path": "M13.983 11.078h2.119c.102 0 .186-.084.186-.186V9.214c0-.102-.084-.186-.186-.186h-2.119c-.102 0-.186.084-.186.186v1.678c0 .102.084.186.186.186zm-2.93 0h2.118c.102 0 .185-.084.185-.186V9.214c0-.102-.083-.186-.185-.186h-2.119c-.101 0-.185.084-.185.186v1.678c0 .102.084.186.185.186zm-2.93 0h2.12c.101 0 .185-.084.185-.186V9.214c0-.102-.084-.186-.185-.186h-2.12c-.101 0-.184.084-.184.186v1.678c0 .102.083.186.184.186zm-2.92 0h2.12c.101 0 .185-.084.185-.186V9.214c0-.102-.084-.186-.185-.186h-2.12c-.101 0-.184.084-.184.186v1.678c0 .102.083.186.184.186zm-2.919 0h2.119c.102 0 .186-.084.186-.186V9.214c0-.102-.084-.186-.186-.186H.284c-.102 0-.186.084-.186.186v1.678c0 .102.084.186.186.186zM15 1.614c-.072 0-.135.033-.183.081-.048.048-.081.111-.081.183v1.678c0 .144.12.264.264.264h2.119c.144 0 .264-.12.264-.264V1.878c0-.144-.12-.264-.264-.264H15zm-2.93 2.92c-.072 0-.135.033-.183.081-.048.048-.081.111-.081.183v1.678c0 .144.12.264.264.264h2.119c.144 0 .264-.12.264-.264V4.878c0-.144-.12-.264-.264-.264H12.07zm-2.93 0c-.072 0-.135.033-.183.081-.048.048-.081.111-.081.183v1.678c0 .144.12.264.264.264h2.119c.144 0 .264-.12.264-.264V4.878c0-.144-.12-.264-.264-.264H9.14z",
        "viewBox": "0 0 24 24"
    },
    "Git": {
        "color": "#F05032",
        "path": "M23.546 10.93L13.07.45a1.8 1.8 0 0 0-2.548 0L9.4 1.568l3.145 3.145a1.69 1.69 0 0 1 2.382 0 1.69 1.69 0 0 1 0 2.382l-3.145 3.145a1.69 1.69 0 0 1-2.096.248l-2.7-2.7a1.69 1.69 0 0 1-.248 2.096L1.575 14.99a1.8 1.8 0 0 0 0 2.548L12.05 28.01a1.8 1.8 0 0 0 2.548 0L25.12 17.54a1.8 1.8 0 0 0 0-2.548zM9.4 10.1l-3.145-3.145a1.69 1.69 0 0 1 0-2.382 1.69 1.69 0 0 1 2.382 0l3.145 3.145a1.69 1.69 0 0 1 0 2.382A1.69 1.69 0 0 1 9.4 10.1z",
        "viewBox": "0 0 24 24"
    }
}

ROW1 = ["Python", "JavaScript", "TypeScript", "C++", "PHP", "Java"]
ROW2 = ["SQL", "React", "Node.js", "Docker", "Git"]

def generate_svg():
    canvas_w = 875
    canvas_h = 160
    titlebar_h = 30
    pad = 24
    
    css = f"""
    .b {{
      transition: all 0.3s cubic-bezier(.2,.8,.2,1);
      stroke: {FRAME};
      fill: #161b22;
      cursor: pointer;
    }}
    .b:hover {{
      stroke: {CYAN};
      fill: #0f2d3a;
      filter: drop-shadow(0px 0px 8px rgba(34, 211, 238, 0.5));
    }}
    .icon {{
      fill: {MUTED};
      transition: all 0.3s ease;
    }}
    .b:hover .icon {{
      fill: var(--hover-color);
      filter: drop-shadow(0px 0px 4px var(--hover-color));
    }}
    .text {{
      fill: {MUTED};
      font-size: 11px;
      font-weight: 700;
      transition: all 0.3s ease;
    }}
    .b:hover .text {{
      fill: {TEXT};
    }}
    """
    
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        # Background
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="{BG}"/>',
        # Border
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        # Titlebar Dots
    ]
    
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{pad + i*16}" cy="{titlebar_h/2}" r="5" fill="{dotcol}"/>')
        
    parts.append(f'<text x="{canvas_w/2}" y="{titlebar_h/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">zulvikar@is-a.dev: ~/skills</text>')
    parts.append(f'<line x1="0" y1="{titlebar_h}" x2="{canvas_w}" y2="{titlebar_h}" stroke="{FRAME}"/>')
    
    # Render Rows of Badges
    badge_w = 110
    badge_h = 34
    badge_rx = 6
    gap = 16
    
    def render_row(row_techs, start_y):
        row_w = len(row_techs) * badge_w + (len(row_techs) - 1) * gap
        start_x = (canvas_w - row_w) / 2
        
        for idx, tech in enumerate(row_techs):
            info = ICONS.get(tech)
            if not info:
                continue
            
            x = start_x + idx * (badge_w + gap)
            y = start_y
            
            # Create a group for hover styling
            parts.append(f'<g style="--hover-color: {info["color"]};">')
            # Badge background rect
            parts.append(f'  <rect class="b" x="{x}" y="{y}" width="{badge_w}" height="{badge_h}" rx="{badge_rx}"/>')
            
            # Badge Icon (placed left-aligned in badge)
            icon_size = 16
            icon_x = x + 12
            icon_y = y + (badge_h - icon_size) / 2
            
            # Render inline svg path for icon
            parts.append(f'  <svg x="{icon_x}" y="{icon_y}" width="{icon_size}" height="{icon_size}" viewBox="{info["viewBox"]}">')
            parts.append(f'    <path class="icon" d="{info["path"]}"/>')
            parts.append(f'  </svg>')
            
            # Badge Text (placed to the right of icon)
            text_x = x + 12 + icon_size + 8
            text_y = y + badge_h / 2 + 4
            parts.append(f'  <text class="text" x="{text_x}" y="{text_y}">{tech}</text>')
            parts.append(f'</g>')
            
    render_row(ROW1, 48)
    render_row(ROW2, 98)
    
    parts.append("</svg>")
    
    with open(OUT_PATH, "w") as f:
        f.write("".join(parts))
    print(f"Successfully generated {OUT_PATH}")

if __name__ == "__main__":
    generate_svg()
