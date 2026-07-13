import requests
import re
import json

SLUGS = {
    "Python": "python",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "C/C++": "cplusplus",
    "PHP": "php",
    "Java": "java",
    "SQL": "postgresql",
    "Next.js": "nextdotjs",
    "React": "react",
    "Laravel": "laravel",
    "Flutter": "flutter",
    "Node.js": "nodedotjs",
    "Tailwind CSS": "tailwindcss",
    "Bootstrap": "bootstrap",
    "MySQL": "mysql",
    "PostgreSQL": "postgresql",
    "MongoDB": "mongodb",
    "Supabase": "supabase",
    "Firebase": "firebase",
    "ESP32": "espressif",
    "Arduino": "arduino",
    "Git": "git",
    "GitHub": "github",
    "Vercel": "vercel",
    "VS Code": "visualstudiocode",
    "Linux": "linux",
    "Postman": "postman",
    "Google Analytics": "googleanalytics",
    "Notion": "notion",
    "Miro": "miro",
    "Oracle Database": "oracle",
    "TensorFlow": "tensorflow",
    "Keras": "keras"
}

paths = {}
for name, slug in SLUGS.items():
    try:
        url = f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        m = re.search(r'd="([^"]+)"', r.text)
        if m:
            paths[name] = m.group(1)
            print(f"Fetched {name}")
    except Exception as e:
        print(f"Error fetching {name}: {e}")

with open("data/paths_data.json", "w") as f:
    json.dump(paths, f, indent=2)
print("Done writing data/paths_data.json")
