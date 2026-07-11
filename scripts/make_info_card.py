import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STATS_PATH = os.path.join(HERE, "..", "data", "stats.json")
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 480, 620
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 200
LINE_H = 20.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"
SECTION = "#58a6ff"
GREEN = "#3fb950"
DEL = "#f85149"
ACCENT = "#22d3ee"

ROWS = [
    ("host",),
    ("kv", "OS",        None, "os"),
    ("kv", "Uptime",    None, "age"),
    ("kv", "Host",      None, "host"),
    ("kv", "Kernel",    None, "kernel"),
    ("kv", "IDE",       None, "ide"),
    ("kv", "EDU",       None, "edu"),
    ("gap",),
    ("sec", "Languages"),
    ("kv", "Languages.Programming", None, "languages_programming"),
    ("kv", "Languages.Real",       None, "languages_real"),
    ("gap",),
    ("sec", "Hobbies"),
    ("kv", "Hobbies.Software", None, "hobbies_software"),
    ("kv", "Hobbies.Life",     None, "hobbies_life"),
    ("gap",),
    ("sec", "Contact"),
    ("kv", "Timezone",       None, "timezone"),
    ("kv", "Email.Personal", None, "email"),
    ("kv", "Portfolio",      None, "portfolio"),
    ("kv", "LinkedIn",       None, "linkedin"),
    ("kv", "TikTok",         None, "tiktok"),
    ("kv", "Discord",        None, "discord"),
    ("gap",),
    ("sec", "GitHub Stats"),
    ("kv", "Repos",     None, "repos_stats"),
    ("kv", "Commits",   None, "commits_stats"),
    ("loc",),
]

DEFAULTS = {
    "os": "Windows 11, Ubuntu",
    "age": "22 years, 2 months, 12 days",
    "host": "OMEN 15",
    "kernel": "Fullstack Dev, Backend, AL/ML",
    "ide": "VScode, Clion, Arduino IDE",
    "edu": "Computer Engineering Student @ POLINES",
    "languages_programming": "Python, JS, TS, C/C++, PHP, Java, SQL",
    "languages_real": "English, Indonesian",
    "hobbies_software": "AI Project, Web Dev, Discord Bot",
    "hobbies_life": "Powerlifting, Gaming, Coffee",
    "timezone": "Asia/Jakarta (WIB)",
    "portfolio": "zulvikar.is-a.dev",
    "email": "zulvikar.kharisma22@gmail.com",
    "linkedin": "in/zulvikar-kharisma",
    "tiktok": "@sleepyinsomniacc_",
    "discord": "dycandx",
}


def esc(s):
    return html.escape(str(s))


def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')


stats = DEFAULTS.copy()
if os.path.exists(STATS_PATH):
    try:
        with open(STATS_PATH) as f:
            loaded = json.load(f)
            stats.update(loaded)
            repo_v = loaded.get("repos", "?")
            contrib_v = loaded.get("contributions", "?")
            star_v = loaded.get("stars", "?")
            stats["repos_stats"] = f"{repo_v}  {{Contributed: {contrib_v}}}  |  Stars: {star_v}"
            commit_v = loaded.get("commits", "?")
            follower_v = loaded.get("followers", "?")
            stats["commits_stats"] = f"{commit_v}  |  Followers: {follower_v}"
            stats["loc_t"] = loaded.get("loc_total", "?")
            stats["loc_a"] = loaded.get("loc_add", "?")
            stats["loc_d"] = loaded.get("loc_del", "?")
    except Exception:
        pass

for key, val in DEFAULTS.items():
    if key not in stats:
        stats[key] = val

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">zulvikar@is-a.dev: ~$ neofetch</text>')

y = TITLEBAR_H + 26
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.4
        continue
    if kind == "host":
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                 f'<tspan fill="{GREEN}">zulvikar</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">is-a.dev</tspan></text>'
                 f'<line x1="{KEY_X+106}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
                 f'&#8212; {title}</text>'
                 f'<line x1="{KEY_X + 12 + len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key_text = esc(row[1])
        val_key = row[3]
        val_text = esc(stats.get(val_key, ""))
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{key_text}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val_text}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>')
    elif kind == "loc":
        loc_t = esc(stats.get("loc_t", "?"))
        loc_a = esc(stats.get("loc_a", "?"))
        loc_d = esc(stats.get("loc_d", "?"))
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">Line of Code</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" font-size="12.5">'
                 f'<tspan fill="{INK}">{loc_t}</tspan>'
                 f'<tspan fill="{GREEN}">  (+{loc_a}++</tspan>'
                 f'<tspan fill="{DEL}">,  -{loc_d}--</tspan>'
                 f'<tspan fill="{INK}">)</tspan>'
                 f'</text>')
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes)")
