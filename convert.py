from playwright.sync_api import sync_playwright
from PIL import Image
import io
import os

SVGS = [
    "dark_mode.svg",
    "light_mode.svg",
]

# Match each SVG's background color so rounded corners don't bleed white
BG_COLORS = {
    "dark_mode.svg": "#161b22",
    "light_mode.svg": "#ffffff",
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for filename in SVGS:
        file_path = f"file://{os.path.abspath(filename)}"
        print(f"Loading {file_path}")

        bg = BG_COLORS.get(filename, "#161b22")
        page = browser.new_page(viewport={"width": 985, "height": 530})
        # Set background to match SVG background so rounded corners are clean
        page.emulate_media(color_scheme="dark" if "dark" in filename else "light")
        page.goto(file_path, wait_until="networkidle")
        page.add_style_tag(content=f"html, body {{ background: {bg} !important; margin: 0; padding: 0; }}")

        frames = []
        for _ in range(30):
            page.wait_for_timeout(100)
            frames.append(page.screenshot(omit_background=False))

        name = filename.replace(".svg", ".webp")
        images = [Image.open(io.BytesIO(f)) for f in frames]
        images[0].save(
            name,
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
        )
        print(f"Saved {name}")
        page.close()

    browser.close()
