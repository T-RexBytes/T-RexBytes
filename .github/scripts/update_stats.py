import re
import urllib.request
import os

USERNAME = "T-RexBytes"
REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
README_PATH = os.path.join(REPO_ROOT, "README.md")
SVG_PATH = os.path.join(REPO_ROOT, "assets", "stats.svg")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_stats():
    stats = {}
    
    # 1. Fetch Streak Stats (Contributions, Current Streak, Longest Streak)
    try:
        url_streak = f"https://streak-stats.demolab.com/?user={USERNAME}"
        req = urllib.request.Request(url_streak, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            
            contrib_match = re.search(r'(\d[\d,]*)\s*</text>\s*</g>\s*<!-- Total Contributions label -->', content)
            current_match = re.search(r'<!-- Current Streak big number -->.*?(\d[\d,]*)\s*</text>', content, re.DOTALL)
            longest_match = re.search(r'<!-- Longest Streak big number -->.*?(\d[\d,]*)\s*</text>', content, re.DOTALL)
            
            if contrib_match:
                stats["contributions"] = contrib_match.group(1).replace(",", "")
            if current_match:
                stats["current_streak"] = current_match.group(1).replace(",", "")
            if longest_match:
                stats["longest_streak"] = longest_match.group(1).replace(",", "")
    except Exception as e:
        print(f"Warning: Failed to fetch streak stats: {e}")

    # 2. Fetch Merged PRs
    try:
        url_prs = f"https://github-readme-stats.vercel.app/api?username={USERNAME}&show=prs_merged"
        req = urllib.request.Request(url_prs, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            prs_match = re.search(r'prs_merged.*?(\d[\d,]*)<\/text>', content, re.DOTALL)
            if prs_match:
                stats["prs_merged"] = prs_match.group(1).replace(",", "")
    except Exception as e:
        print(f"Warning: Failed to fetch PR stats: {e}")

    return stats

def generate_svg(contributions, prs_merged, longest_streak, current_streak):
    svg_template = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 160" width="440" height="160" fill="none">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
      .term-bg {{
        fill: #0d1117;
        stroke: #30363d;
        stroke-width: 1.5;
        rx: 10px;
      }}
      .label-idx {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 13px;
        font-weight: 600;
        fill: #7d8590;
      }}
      .label-text {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 13px;
        font-weight: 500;
        fill: #e6edf3;
      }}
      .colon {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 13px;
        font-weight: 700;
        fill: #58a6ff;
      }}
      .val-contrib {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 14px;
        font-weight: 700;
        fill: #2ea44f;
      }}
      .val-prs {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 14px;
        font-weight: 700;
        fill: #a371f7;
      }}
      .val-longest {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 14px;
        font-weight: 700;
        fill: #26a641;
      }}
      .val-current {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        font-size: 14px;
        font-weight: 700;
        fill: #39d353;
      }}
      .unit {{
        font-size: 11px;
        font-weight: 400;
        fill: #8b949e;
      }}
      .dot-green {{ fill: #39d353; }}
      .dot-green-dim {{ fill: #26a641; }}
      .dot-green-dark {{ fill: #006d32; }}
      .dot-green-darker {{ fill: #0e4429; }}
    </style>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Terminal Window Background -->
  <rect x="1" y="1" width="438" height="158" class="term-bg" />

  <!-- Window Header Bar -->
  <rect x="1" y="1" width="438" height="28" fill="#161b22" rx="10" />
  <rect x="1" y="20" width="438" height="9" fill="#161b22" />
  <line x1="1" y1="29" x2="439" y2="29" stroke="#30363d" stroke-width="1" />

  <!-- Terminal Window Controls -->
  <circle cx="16" cy="15" r="4.5" fill="#f85149" />
  <circle cx="30" cy="15" r="4.5" fill="#e3b341" />
  <circle cx="44" cy="15" r="4.5" fill="#2ea043" />

  <!-- Header Title / Contribution Graph Accents -->
  <g transform="translate(355, 11)">
    <rect x="0" y="0" width="8" height="8" rx="1.5" class="dot-green-darker" />
    <rect x="11" y="0" width="8" height="8" rx="1.5" class="dot-green-dark" />
    <rect x="22" y="0" width="8" height="8" rx="1.5" class="dot-green-dim" />
    <rect x="33" y="0" width="8" height="8" rx="1.5" class="dot-green" filter="url(#glow)" />
  </g>

  <!-- Row 1: Total Contributions -->
  <g transform="translate(20, 56)">
    <text class="label-idx" x="0" y="0">i.</text>
    <text class="label-text" x="32" y="0">total contributions</text>
    <text class="colon" x="222" y="0">:</text>
    <text class="val-contrib" x="242" y="0">{contributions}</text>
  </g>

  <!-- Row 2: Total Pull-Req Merged -->
  <g transform="translate(20, 84)">
    <text class="label-idx" x="0" y="0">ii.</text>
    <text class="label-text" x="32" y="0">total pull-req merged</text>
    <text class="colon" x="222" y="0">:</text>
    <text class="val-prs" x="242" y="0">{prs_merged}</text>
  </g>

  <!-- Row 3: Longest Streak -->
  <g transform="translate(20, 112)">
    <text class="label-idx" x="0" y="0">iii.</text>
    <text class="label-text" x="32" y="0">longest streak</text>
    <text class="colon" x="222" y="0">:</text>
    <text class="val-longest" x="242" y="0">{longest_streak} <tspan class="unit">days</tspan></text>
  </g>

  <!-- Row 4: Current Streak -->
  <g transform="translate(20, 140)">
    <text class="label-idx" x="0" y="0">iv.</text>
    <text class="label-text" x="32" y="0">current streak</text>
    <text class="colon" x="222" y="0">:</text>
    <text class="val-current" x="242" y="0" filter="url(#glow)">{current_streak} <tspan class="unit">days</tspan></text>
    <text x="315" y="-1" font-size="12">🔥</text>
  </g>
</svg>
'''
    os.makedirs(os.path.dirname(SVG_PATH), exist_ok=True)
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print("assets/stats.svg successfully updated!")

def update_all():
    stats = fetch_stats()
    print("Fetched stats:", stats)

    # Fallbacks
    contributions = stats.get("contributions", "727")
    prs_merged = stats.get("prs_merged", "67")
    longest_streak = stats.get("longest_streak", "36")
    current_streak = stats.get("current_streak", "24")

    # Update SVG
    generate_svg(contributions, prs_merged, longest_streak, current_streak)

if __name__ == "__main__":
    update_all()
