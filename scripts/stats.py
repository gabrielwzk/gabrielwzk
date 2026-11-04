"""Busca dados reais na API do GitHub e gera assets/stats.svg"""
import json, os, urllib.request

USER = os.environ["GH_USER"]
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                 headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(req))

def count(q):
    return api(f"/search/issues?q={q}&per_page=1")["total_count"]

repos = api(f"/users/{USER}/repos?per_page=100&type=owner")
stars = sum(r["stargazers_count"] for r in repos)
prs = count(f"author:{USER}+type:pr")
issues = count(f"author:{USER}+type:issue")
commits = api(f"/search/commits?q=author:{USER}&per_page=1")["total_count"]

langs = {}
for r in repos:
    if not r["fork"] and r["language"]:
        langs[r["language"]] = langs.get(r["language"], 0) + 1
total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda x: -x[1])[:4]

F = "font-family=\"'Courier New',monospace\""
rows = "".join(
    f'<text x="40" y="{70+i*26}" fill="#888" {F} font-size="13">{n}</text>'
    f'<text x="270" y="{70+i*26}" fill="#fff" {F} font-size="13" text-anchor="end">{v}</text>'
    f'<line x1="40" x2="270" y1="{76+i*26}" y2="{76+i*26}" stroke="#444" stroke-dasharray="3"/>'
    for i, (n, v) in enumerate([("Commits", commits), ("Pull requests", prs), ("Issues", issues), ("Estrelas", stars)])
)
lrows = "".join(
    f'<rect x="330" y="{60+i*30}" width="{240*q/total}" height="10" fill="#fff"/>'
    f'<text x="330" y="{55+i*30}" fill="#fff" {F} font-size="12">{l} · {100*q/total:.0f}%</text>'
    for i, (l, q) in enumerate(top)
)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 190" width="100%">
<rect width="640" height="190" fill="#000"/>
<rect x="2" y="2" width="636" height="186" fill="none" stroke="#fff" stroke-width="3"/>
<text x="40" y="38" fill="#fff" {F} font-size="16">STATUS</text>
<text x="330" y="38" fill="#fff" {F} font-size="16">MAGIAS</text>
{rows}{lrows}
</svg>'''
open("assets/stats.svg", "w", encoding="utf-8").write(svg)
