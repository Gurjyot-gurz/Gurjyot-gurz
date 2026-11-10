#!/usr/bin/env python3
import json, os, html, urllib.request
from datetime import datetime
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "Gurjyot-gurz")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = Path("assets/profile")
OUT.mkdir(parents=True, exist_ok=True)

QUERY = '''
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
'''

def calendar():
    body = json.dumps({"query": QUERY, "variables": {"login": USERNAME}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
        "User-Agent": "github-profile-readme-generator"
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.load(response)
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

def shell(w, h, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><style>
.serif{{font-family:Georgia,'Times New Roman',serif}}
.mono{{font-family:'Courier New',monospace;letter-spacing:1.5px}}
.ink{{fill:#10131B}} .muted{{fill:#737987}} .blue{{fill:#247BFF}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
.fade{{animation:rise .8s ease both}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style></defs>{body}</svg>'''

def save(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")

def main():
    cal = calendar()
    total = cal["totalContributions"]
    save("hero.svg", shell(1000, 180, f'''
<rect x="1" y="1" width="998" height="178" rx="18" fill="#F5F4F0" stroke="#E4E2DC"/>
<rect x="30" y="28" width="8" height="8" rx="2" fill="#247BFF"/>
<text x="52" y="36" class="mono muted" font-size="11">CLOUD • DEVOPS • AUTOMATION • AI</text>
<text x="30" y="96" class="serif ink fade" font-size="56">Gurjyot Singh</text>
<text x="32" y="126" class="mono muted" font-size="12">BUILDING PRACTICAL SYSTEMS, ONE COMMIT AT A TIME.</text>
<text x="32" y="154" class="serif blue" font-size="20" font-style="italic">{total:,} contributions in the last year</text>
<circle cx="855" cy="88" r="55" fill="#E7ECF7"/><text x="855" y="107" text-anchor="middle" class="serif blue" font-size="54">G</text>
<path d="M785 146 Q855 113 925 146" fill="none" stroke="#247BFF" stroke-width="2" opacity=".35"/>
'''))

    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["contributionCount"]
    keys = sorted(monthly)[-12:]
    maxv = max([monthly[k] for k in keys] + [1])
    bars = []
    for i, key in enumerate(keys):
        value = monthly[key]
        x, h = 34 + i * 78, max(4, round(82 * value / maxv))
        y = 133 - h
        label = datetime.strptime(key, "%Y-%m").strftime("%b")
        fill = "#247BFF" if value == maxv and value else "#B8C9F5"
        bars.append(f'<rect x="{x}" y="{y}" width="44" height="{h}" rx="5" fill="{fill}"><animate attributeName="height" from="0" to="{h}" dur=".7s" begin="{i*.05:.2f}s" fill="freeze"/></rect>')
        bars.append(f'<text x="{x+22}" y="155" text-anchor="middle" class="mono muted" font-size="9">{label}</text>')
        bars.append(f'<text x="{x+22}" y="{max(20,y-6)}" text-anchor="middle" class="mono ink" font-size="9">{value}</text>')
    save("activity.svg", shell(1000, 205, f'''
<rect x="1" y="1" width="998" height="203" rx="18" fill="#F5F4F0" stroke="#E4E2DC"/>
<text x="28" y="34" class="mono muted" font-size="10">THE LAST 12 MONTHS ON GITHUB</text>
<text x="28" y="76" class="serif ink" font-size="38">{total:,} contributions</text>
<text x="28" y="98" class="mono muted" font-size="9">MONTHLY ACTIVITY</text>
{''.join(bars)}
<line x1="28" y1="134" x2="972" y2="134" stroke="#D9D8D2"/>
'''))

    cells = []
    for i, day in enumerate(days):
        x, y, n = 26 + (i // 7) * 14, 39 + (i % 7) * 14, day["contributionCount"]
        color = "#E5E8EF" if n == 0 else "#B7CBFF" if n < 3 else "#6D9EFF" if n < 6 else "#247BFF"
        cells.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{color}"><title>{html.escape(day["date"])}: {n} contributions</title></rect>')
    save("heatmap.svg", shell(1000, 170, f'''
<rect x="1" y="1" width="998" height="168" rx="18" fill="#F5F4F0" stroke="#E4E2DC"/>
<text x="26" y="25" class="mono muted" font-size="10">CONSISTENCY IS BUILT ONE DAY AT A TIME</text>
{''.join(cells)}
<text x="26" y="155" class="mono muted" font-size="9">LESS</text>
<rect x="62" y="145" width="10" height="10" rx="2" fill="#E5E8EF"/>
<rect x="78" y="145" width="10" height="10" rx="2" fill="#B7CBFF"/>
<rect x="94" y="145" width="10" height="10" rx="2" fill="#6D9EFF"/>
<rect x="110" y="145" width="10" height="10" rx="2" fill="#247BFF"/>
<text x="130" y="155" class="mono muted" font-size="9">MORE</text>
'''))
    print(f"Rendered {total} contributions for {USERNAME}")

if __name__ == "__main__":
    main()
