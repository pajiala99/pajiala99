"""Build the animated SVGs shown on the GitHub profile README.

Writes assets/header-{dark,light}.svg and assets/stats-{dark,light}.svg.
The header is static content; the stats card reads live numbers from the
GitHub GraphQL API, so it needs GITHUB_TOKEN in the environment (the
profile-assets workflow passes the Actions token; locally, use
`GITHUB_TOKEN=$(gh auth token) python3 scripts/build_assets.py`).
"""
import json
import os
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "pajiala99"
HACKATHONS = 3  # BIOS V2 (won), Smart India Hackathon, Homingo
SKIP_REPOS = {USER}  # the profile repo itself
SKIP_LANGS = {"TeX", "Makefile", "Jupyter Notebook"}
OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(bg1="#0b1020", bg2="#161d38", text="#ece8dd", muted="#8f97ad",
                 accent="#d4a94c", line="#2a3356", node="#1b2445", track="#222b4a"),
    "light": dict(bg1="#fbf8f1", bg2="#f1ece0", text="#1d2235", muted="#5f6578",
                  accent="#a87a1e", line="#d8d0bd", node="#ffffff", track="#e6dfcf"),
}
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def header_svg(t):
    roles = ["Backend APIs", "Data pipelines", "Machine-learning models", "AI agents", "Apps people use"]
    n, cycle = len(roles), 2.6
    role_css = "".join(
        f".r{i}{{animation:role {n * cycle}s {i * cycle}s infinite both}}" for i in range(n))
    role_txt = "".join(
        f'<text class="role r{i}" x="64" y="228">{escape(r)}</text>' for i, r in enumerate(roles))

    nodes = [("API", 760, 210), ("Pipeline", 870, 120), ("Model", 990, 190), ("Agent", 1090, 100), ("App", 1150, 220)]
    path = "M " + " L ".join(f"{x} {y}" for _, x, y in nodes)
    circles = "".join(
        f'<g class="node" style="animation-delay:{0.25 + i * 0.15:.2f}s">'
        f'<circle cx="{x}" cy="{y}" r="27" /><text x="{x}" y="{y + 4}">{lab}</text></g>'
        for i, (lab, x, y) in enumerate(nodes))
    dots = "".join(
        f'<circle class="pulse" r="5"><animateMotion dur="5s" begin="{b}s" repeatCount="indefinite" path="{path}" /></circle>'
        for b in (0, 1.7, 3.4))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="Hardik Pajiala: I build the whole system">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="{t['line']}"/></pattern>
</defs>
<style>
  .name{{font:700 64px {SERIF};fill:{t['text']};animation:rise .9s ease-out both}}
  .tag{{font:600 26px {SANS};fill:{t['accent']};animation:rise .9s .2s ease-out both}}
  .pre{{font:500 15px {MONO};fill:{t['muted']};letter-spacing:.14em;animation:rise .9s .1s ease-out both}}
  .role{{font:500 24px {SANS};fill:{t['text']};opacity:0}}
  .foot{{font:500 14px {MONO};fill:{t['muted']};letter-spacing:.06em;animation:rise .9s .4s ease-out both}}
  .wire{{fill:none;stroke:{t['accent']};stroke-width:2;stroke-dasharray:6 7;opacity:.55;animation:flow 1.6s linear infinite}}
  .node circle{{fill:{t['node']};stroke:{t['accent']};stroke-width:2}}
  .node text{{font:600 12px {SANS};fill:{t['text']};text-anchor:middle}}
  .node{{animation:pop .6s ease-out both}}
  .pulse{{fill:{t['accent']}}}
  .caret{{fill:{t['accent']};animation:blink 1s steps(1) infinite}}
  {role_css}
  @keyframes role{{0%{{opacity:0;transform:translateY(10px)}}4%,16%{{opacity:1;transform:none}}20%,100%{{opacity:0;transform:translateY(-10px)}}}}
  @keyframes rise{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
  @keyframes pop{{from{{opacity:0;transform:scale(.6)}}to{{opacity:1;transform:none}}}}
  @keyframes flow{{to{{stroke-dashoffset:-26}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  .node{{transform-box:fill-box;transform-origin:center}}
  @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.r0{{opacity:1}}.pulse{{display:none}}}}
</style>
<rect width="1200" height="300" rx="18" fill="url(#bg)"/>
<rect width="1200" height="300" rx="18" fill="url(#grid)" opacity=".5"/>
<text class="pre" x="64" y="70">COMPUTER ENGINEERING · THAPAR INSTITUTE · CLASS OF 2028</text>
<text class="name" x="62" y="138">Hardik Pajiala</text>
<text class="tag" x="64" y="182">I build the whole system:</text>
{role_txt}
<rect class="caret" x="64" y="246" width="34" height="3" rx="1.5"/>
<text class="foot" x="64" y="276">pajiala99.github.io</text>
<path class="wire" d="{path}"/>
{dots}
{circles}
</svg>
"""


def fetch_stats(token):
    query = """query($login:String!){user(login:$login){
      contributionsCollection{contributionCalendar{totalContributions}}
      repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){
        totalCount nodes{name languages(first:12,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        user = json.load(r)["data"]["user"]
    langs, colors = {}, {}
    repos = [n for n in user["repositories"]["nodes"] if n["name"] not in SKIP_REPOS]
    for repo in repos:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name in SKIP_LANGS:
                continue
            langs[name] = langs.get(name, 0) + e["size"]
            colors[name] = e["node"]["color"] or "#888888"
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    return {
        "contributions": user["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "repos": len(repos),
        "languages": [(name, size / total, colors[name]) for name, size in top],
    }


def stats_svg(t, s):
    tiles = [(str(s["contributions"]), "contributions", "in the last year"),
             (str(s["repos"]), "public projects", "on this profile"),
             (str(HACKATHONS), "hackathons", "one problem statement won")]
    tile_svg = "".join(
        f'<g class="tile" style="animation-delay:{i * 0.12:.2f}s" transform="translate({40 + i * 170} 54)">'
        f'<text class="big" y="44">{v}</text><text class="lab" y="72">{a}</text><text class="sub" y="92">{b}</text></g>'
        for i, (v, a, b) in enumerate(tiles))

    bar_x, bar_w, x, segs, legend = 580, 580, 0.0, [], []
    for i, (name, frac, color) in enumerate(s["languages"]):
        w = max(frac * bar_w, 3)
        segs.append(f'<rect class="seg" style="animation-delay:{0.3 + i * 0.08:.2f}s" x="{bar_x + x:.1f}" y="74" width="{w:.1f}" height="14" fill="{color}"/>')
        x += w
        lx, ly = bar_x + (i % 3) * 196, 120 + (i // 3) * 30
        legend.append(f'<g class="leg" style="animation-delay:{0.5 + i * 0.08:.2f}s"><circle cx="{lx + 6}" cy="{ly - 4}" r="6" fill="{color}"/>'
                      f'<text class="ln" x="{lx + 20}" y="{ly + 1}">{escape(name)} <tspan class="pct">{frac * 100:.1f}%</tspan></text></g>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="200" viewBox="0 0 1200 200" role="img" aria-label="GitHub stats for {USER}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
  <clipPath id="barclip"><rect x="{bar_x}" y="74" width="{bar_w}" height="14" rx="7"/></clipPath>
</defs>
<style>
  .h{{font:600 13px {MONO};fill:{t['muted']};letter-spacing:.14em}}
  .big{{font:700 40px {SERIF};fill:{t['accent']}}}
  .lab{{font:600 16px {SANS};fill:{t['text']}}}
  .sub{{font:400 13px {SANS};fill:{t['muted']}}}
  .ln{{font:500 14px {SANS};fill:{t['text']}}}
  .pct{{fill:{t['muted']}}}
  .tile,.leg{{animation:rise .7s ease-out both}}
  .seg{{transform-box:fill-box;transform-origin:left;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}}
  @keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1}}}}
  @keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
  @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="1200" height="200" rx="18" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="1199" height="199" rx="18" fill="none" stroke="{t['line']}"/>
<text class="h" x="40" y="42">AT A GLANCE</text>
<text class="h" x="{bar_x}" y="42">LANGUAGES ACROSS MY REPOS</text>
{tile_svg}
<rect x="{bar_x}" y="74" width="{bar_w}" height="14" rx="7" fill="{t['track']}"/>
<g clip-path="url(#barclip)">{''.join(segs)}</g>
{''.join(legend)}
</svg>
"""


def main():
    OUT.mkdir(exist_ok=True)
    token = os.environ.get("GITHUB_TOKEN")
    stats = fetch_stats(token) if token else None
    for mode, theme in THEMES.items():
        (OUT / f"header-{mode}.svg").write_text(header_svg(theme), encoding="utf-8")
        if stats:
            (OUT / f"stats-{mode}.svg").write_text(stats_svg(theme, stats), encoding="utf-8")
    print("header written" + (f"; stats: {stats['contributions']} contributions, {stats['repos']} repos" if stats else "; no GITHUB_TOKEN, stats skipped"))


if __name__ == "__main__":
    main()
