"""Build the animated SVGs shown on the GitHub profile README.

Writes a dark and a light version of each image into assets/:
  header-*.svg           name, tagline and an API -> App system diagram
  stats-*.svg            results, public projects and languages across repos
  card-<project>-*.svg   one animated card per selected build
Only the stats card reads live data (the GitHub GraphQL API), so it needs
GITHUB_TOKEN in the environment: the profile workflow passes the Actions
token; locally, use `GITHUB_TOKEN=$(gh auth token) python3 scripts/build_assets.py`.

Animation is CSS or SMIL. Nothing animates a CSS transform on an element
that also has a transform attribute: Safari lets the animation replace the
attribute, which stacked every stats tile at 0,0 once.
"""
import itertools
import json
import math
import os
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "pajiala99"
HACKATHONS = 3  # BIOS 2026 (first place), Smart India Hackathon, Homingo
SKIP_REPOS = {USER}  # the profile repo itself
SKIP_LANGS = {"TeX", "Makefile", "Jupyter Notebook"}
OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(bg1="#0b1020", bg2="#161d38", text="#ece8dd", muted="#8f97ad",
                 accent="#d4a94c", line="#2a3356", node="#1b2445", track="#222b4a",
                 ok="#3fb950", bad="#f85149", s2="#4fc7e0", s3="#a98bff",
                 bronze="#cd7f32", silver="#c9ccd6"),
    "light": dict(bg1="#fbf8f1", bg2="#f1ece0", text="#1d2235", muted="#5f6578",
                  accent="#a87a1e", line="#d8d0bd", node="#ffffff", track="#e6dfcf",
                  ok="#1a7f37", bad="#cf222e", s2="#1b7f99", s3="#6f52d9",
                  bronze="#a0612a", silver="#7d8291"),
}
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# FoodBridge demo scores (rows: donations in urgency order, columns: shelters),
# the same matrix as the matcher demo on the portfolio.
FOOD = [[.95, .90, .30, .25], [.92, .35, .28, .20], [.40, .88, .50, .30], [.30, .45, .85, .60]]


def attr(s):
    return escape(s, {'"': "&quot;"})


def kt(*times):
    return ";".join(f"{round(x, 3):g}" for x in times)


def anim(name, values, times, dur, begin="0s"):
    assert len(values) == len(times), (name, values, times)
    return (f'<animate attributeName="{name}" values="{";".join(str(v) for v in values)}" '
            f'keyTimes="{kt(*times)}" dur="{dur}s" begin="{begin}" repeatCount="indefinite"/>')


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
      repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){
        nodes{name languages(first:12,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}"""
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
        "repos": len(repos),
        "languages": [(name, size / total, colors[name]) for name, size in top],
    }


def stats_svg(t, s):
    tiles = [("1st", "place, BIOS 2026", "with SafeTrail"),
             (str(HACKATHONS), "hackathons", "BIOS · SIH · Homingo"),
             (str(s["repos"]), "public projects", "on this profile")]
    # Tiles are placed with plain x/y, never a transform: in Safari a CSS animation
    # can replace an SVG transform attribute and stack every tile at 0,0.
    tile_svg = "".join(
        f'<g class="tile" style="animation-delay:{i * 0.12:.2f}s">'
        f'<text class="big" x="{40 + i * 170}" y="98">{v}</text>'
        f'<text class="lab" x="{40 + i * 170}" y="126">{a}</text>'
        f'<text class="sub" x="{40 + i * 170}" y="146">{b}</text></g>'
        for i, (v, a, b) in enumerate(tiles))

    bar_x, bar_w, x, segs, legend = 580, 580, 0.0, [], []
    for i, (name, frac, color) in enumerate(s["languages"]):
        w = max(frac * bar_w, 3)
        segs.append(f'<rect class="seg" style="animation-delay:{0.3 + i * 0.08:.2f}s" x="{bar_x + x:.1f}" y="74" width="{w:.1f}" height="14" fill="{color}"/>')
        x += w
        lx, ly = bar_x + (i % 3) * 196, 120 + (i // 3) * 30
        legend.append(f'<g class="leg" style="animation-delay:{0.5 + i * 0.08:.2f}s"><circle cx="{lx + 6}" cy="{ly - 4}" r="6" fill="{color}"/>'
                      f'<text class="ln" x="{lx + 20}" y="{ly + 1}">{escape(name)} <tspan class="pct">{frac * 100:.1f}%</tspan></text></g>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="200" viewBox="0 0 1200 200" role="img" aria-label="At a glance: first place at BIOS 2026, {HACKATHONS} hackathons, {s['repos']} public projects, and languages across my repos">
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
  .tile,.leg{{animation:fade .7s ease-out both}}
  .seg{{transform-box:fill-box;transform-origin:left;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}}
  @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
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


# ---------------------------------------------------------------- project cards

def card(t, title, sub, body, foot, tag="", pill=""):
    if pill:
        w = round(len(pill) * 7.4 + 24)
        corner = (f'<rect x="{572 - w}" y="22" width="{w}" height="26" rx="13" fill="{t["accent"]}" fill-opacity=".12" stroke="{t["accent"]}"/>'
                  f'<text class="pill" x="{572 - w / 2:.0f}" y="39" text-anchor="middle">{escape(pill)}</text>')
    else:
        corner = f'<text class="tag" x="572" y="40" text-anchor="end">{escape(tag)}</text>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="340" viewBox="0 0 600 340" role="img" aria-label="{attr(title)}: {attr(sub)}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient></defs>
<style>
  .title{{font:700 24px {SERIF};fill:{t['text']}}}
  .sub{{font:400 14px {SANS};fill:{t['muted']}}}
  .tag{{font:500 12px {MONO};fill:{t['muted']}}}
  .pill{{font:700 11px {MONO};fill:{t['accent']};letter-spacing:.06em}}
  .lane{{font:500 12px {MONO};fill:{t['muted']}}}
  .small{{font:500 11px {MONO};fill:{t['muted']}}}
  .chip{{font:700 10px {MONO};fill:{t['text']}}}
  .foot{{font:500 12px {MONO};fill:{t['text']}}}
  .acc{{fill:{t['accent']}}}
</style>
<rect width="600" height="340" rx="16" fill="url(#bg)"/>
<rect x=".5" y=".5" width="599" height="339" rx="16" fill="none" stroke="{t['line']}"/>
<text class="title" x="28" y="46">{escape(title)}</text>
<text class="sub" x="28" y="70">{escape(sub)}</text>
{corner}
{body}
<line x1="28" y1="296" x2="572" y2="296" stroke="{t['line']}"/>
<text class="foot" x="28" y="321"><tspan class="acc">▸ </tspan>{escape(foot)}</text>
</svg>
"""


def body_safetrail(t):
    """SOS calls queue on the phone through a no-signal gap, then reach the responder."""
    D, X0, X1 = 8, 120, 572
    f = lambda x: (x - X0) / (X1 - X0)  # when the sweeping cursor reaches x
    out = []
    for name, y in (("phone", 130), ("responder", 245)):
        out.append(f'<text class="lane" x="28" y="{y + 4}">{name}</text>'
                   f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{t["line"]}"/>')
    out.append(f'<text class="lane" x="28" y="189">signal</text>'
               f'<line x1="{X0}" y1="185" x2="238" y2="185" stroke="{t["ok"]}" stroke-width="6" stroke-linecap="round"/>'
               f'<line x1="248" y1="185" x2="384" y2="185" stroke="{t["bad"]}" stroke-width="2" stroke-dasharray="4 6"/>'
               f'<text class="small" x="316" y="174" text-anchor="middle" style="fill:{t["bad"]}">no signal</text>'
               f'<line x1="394" y1="185" x2="{X1}" y2="185" stroke="{t["ok"]}" stroke-width="6" stroke-linecap="round"/>')
    out.append(f'<text class="small" x="{X1}" y="113" text-anchor="end" style="fill:{t["accent"]}" opacity="0">saved on phone, retrying'
               + anim("opacity", [0, 0, 1, 1, 0, 0], [0, f(270), f(270) + .01, .62, .63, 1], D) + '</text>')
    out.append(f'<text class="small" x="{X1}" y="229" text-anchor="end" style="fill:{t["ok"]}" opacity="0">delivered ✓'
               + anim("opacity", [0, 0, 1, 1, 0], [0, .70, .71, .96, 1], D) + '</text>')
    for x, (dx, dy), (m0, m1) in ((270, (160, 115), (.62, .70)), (330, (146, 115), (.66, .74))):
        a = f(x)
        out.append('<g opacity="0">' + anim("opacity", [0, 0, 1, 1, 0], [0, a, a + .01, .96, 1], D)
                   + f'<animateMotion path="M0 0 L{dx} {dy}" keyPoints="0;0;1;1" keyTimes="{kt(0, m0, m1, 1)}" calcMode="linear" dur="{D}s" repeatCount="indefinite"/>'
                   + f'<rect x="{x - 20}" y="120" width="40" height="20" rx="10" fill="{t["accent"]}">'
                   + anim("fill", [t["accent"], t["accent"], t["ok"], t["ok"]], [0, m1 - .01, m1, 1], D) + '</rect>'
                   + f'<text class="chip" x="{x}" y="134" text-anchor="middle" style="fill:{t["bg1"]}">SOS</text></g>')
    out.append(f'<line x1="{X0}" y1="102" x2="{X0}" y2="262" stroke="{t["accent"]}" stroke-width="1.5" opacity=".55">'
               + anim("x1", [X0, X1], [0, 1], D) + anim("x2", [X0, X1], [0, 1], D) + '</line>')
    return "".join(out)


def body_cricket(t):
    """Rows flow bronze -> silver -> gold; a bad row stops at the quality gate."""
    D = 6
    zones = (("bronze", 120, 250, t["bronze"]), ("silver", 290, 420, t["silver"]), ("gold", 460, 572, t["accent"]))
    out = ['<text class="lane" x="28" y="168">JSON</text>']
    for name, a, b, c in zones:
        out.append(f'<rect x="{a}" y="110" width="{b - a}" height="98" rx="10" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-opacity=".4"/>'
                   f'<text class="small" x="{(a + b) / 2:.0f}" y="128" text-anchor="middle" style="fill:{c}">{name}</text>')
    for x, label in ((270, "quality gate"), (440, "MERGE")):
        out.append(f'<line x1="{x}" y1="104" x2="{x}" y2="214" stroke="{t["accent"]}" stroke-width="1.5" stroke-dasharray="3 4"/>'
                   f'<text class="small" x="{x}" y="230" text-anchor="middle">{label}</text>')
    out.append(f'<rect x="244" y="244" width="52" height="22" rx="5" fill="{t["bad"]}" fill-opacity=".1" stroke="{t["bad"]}" stroke-opacity=".6"/>'
               f'<text class="small" x="304" y="259" style="fill:{t["bad"]}">quarantined</text>')
    pos = lambda x: (x - 60) / 520  # when a block's left edge reaches x
    g1, g2 = pos(270 - 11), pos(440 - 11)
    fills = [t["bronze"], t["bronze"], t["silver"], t["silver"], t["accent"], t["accent"]]
    for k in range(6):
        out.append(f'<rect x="60" y="158" width="22" height="12" rx="3" fill="{t["bronze"]}" opacity="0">'
                   + anim("x", [60, 580], [0, 1], D, f"-{k}s")
                   + anim("fill", fills, [0, g1, g1 + .01, g2, g2 + .01, 1], D, f"-{k}s")
                   + anim("opacity", [0, 1, 1, 0], [0, .04, .94, 1], D, f"-{k}s") + '</rect>')
    stop = pos(248)
    out.append(f'<rect x="60" y="158" width="22" height="12" rx="3" fill="{t["bad"]}" opacity="0">'
               + anim("x", [60, 248, 248], [0, stop, 1], D, "-2.5s")
               + anim("y", [158, 158, 249, 249], [0, stop + .06, stop + .16, 1], D, "-2.5s")
               + anim("opacity", [0, 1, 1, 0, 0], [0, .04, .86, .93, 1], D, "-2.5s") + '</rect>')
    return "".join(out)


def matchings(m):
    """Greedy (each donation, most urgent first, takes its best free shelter) vs the optimum."""
    n, taken, greedy = len(m), set(), []
    for row in m:
        j = max((j for j in range(n) if j not in taken), key=row.__getitem__)
        taken.add(j)
        greedy.append(j)
    total = lambda p: sum(m[i][p[i]] for i in range(n))
    best = list(max(itertools.permutations(range(n)), key=total))
    return greedy, best, total(greedy), total(best)


def body_foodbridge(t):
    """Greedy draws its matches first; then the optimal assignment replaces them."""
    D = 10
    greedy, best, g, h = matchings(FOOD)
    ys = [118, 156, 194, 232]
    out = ['<text class="small" x="170" y="98" text-anchor="middle">donations, most urgent first</text>'
           '<text class="small" x="430" y="98" text-anchor="middle">shelters</text>']

    def link(i, j, color, start, fade_at, weak):
        x1, y1, x2, y2 = 184, ys[i], 416, ys[j]
        length = round(math.hypot(x2 - x1, y2 - y1), 1)
        s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.5" stroke-linecap="round" '
             f'stroke-dasharray="{length}" stroke-dashoffset="{length}">'
             + anim("stroke-dashoffset", [length, length, 0, 0], [0, start, start + .06, 1], D)
             + anim("opacity", [1, 1, 0, 0], [0, fade_at, fade_at + .03, 1], D) + '</line>')
        if weak:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 7
            s += (f'<text class="small" x="{mx:.0f}" y="{my:.0f}" text-anchor="middle" style="fill:{t["bad"]}" opacity="0">{FOOD[i][j]:.2f}'
                  + anim("opacity", [0, 0, 1, 1, 0, 0], [0, start + .06, start + .07, fade_at, fade_at + .03, 1], D) + '</text>')
        return s

    for k, j in enumerate(greedy):
        weak = FOOD[k][j] < .4
        out.append(link(k, j, t["bad"] if weak else t["muted"], .04 + .08 * k, .44, weak))
    for k, j in enumerate(best):
        out.append(link(k, j, t["ok"], .52 + .08 * k, .94, False))
    for k, y in enumerate(ys):
        out.append(f'<circle cx="170" cy="{y}" r="14" fill="{t["node"]}" stroke="{t["accent"]}" stroke-width="2"/>'
                   f'<text class="chip" x="170" y="{y + 4}" text-anchor="middle">{"ABCD"[k]}</text>'
                   f'<rect x="416" y="{y - 14}" width="28" height="28" rx="6" fill="{t["node"]}" stroke="{t["s2"]}" stroke-width="2"/>'
                   f'<text class="chip" x="430" y="{y + 4}" text-anchor="middle">S{k + 1}</text>')
    out.append(f'<text class="small" x="300" y="274" text-anchor="middle" style="fill:{t["text"]}" opacity="0">greedy: most urgent picks first · total {g:.2f}'
               + anim("opacity", [0, 1, 1, 0, 0], [0, .02, .44, .47, 1], D) + '</text>')
    out.append(f'<text class="small" x="300" y="274" text-anchor="middle" style="fill:{t["ok"]}" opacity="0">Hungarian: best overall · total {h:.2f}'
               + anim("opacity", [0, 0, 1, 1, 0, 0], [0, .5, .52, .94, .97, 1], D) + '</text>')
    return "".join(out), g, h


def body_timetable(t):
    """Classes get coloured one by one; each colour is a time slot in the grid."""
    D = 9
    cx, cy, r = 190, 190, 70
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]
    names = ["DSA", "OS", "DB", "ML", "SE", "CN"]
    edges = [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 4)]
    slot = [0, 1, 2, 0, 2, 1]
    assert all(slot[a] != slot[b] for a, b in edges), "the example colouring must be valid"
    colors = [t["accent"], t["s2"], t["s3"]]
    out = [f'<line x1="{pts[a][0]:.0f}" y1="{pts[a][1]:.0f}" x2="{pts[b][0]:.0f}" y2="{pts[b][1]:.0f}" stroke="{t["line"]}" stroke-width="2"/>'
           for a, b in edges]
    cols = [330, 412, 494]
    for c, (x, label) in enumerate(zip(cols, ["Mon 9:00", "Mon 10:00", "Tue 9:00"])):
        out.append(f'<text class="small" x="{x + 37}" y="116" text-anchor="middle" style="fill:{colors[c]}">{label}</text>'
                   f'<rect x="{x}" y="124" width="74" height="78" rx="8" fill="none" stroke="{t["line"]}"/>')
    used = [0, 0, 0]
    for k, ((x, y), name, c) in enumerate(zip(pts, names, slot)):
        tk = .06 + .09 * k
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="17" fill="{t["node"]}" stroke="{t["muted"]}" stroke-width="1.5">'
                   + anim("fill", [t["node"], t["node"], colors[c], colors[c], t["node"], t["node"]], [0, tk, tk + .02, .92, .95, 1], D) + '</circle>'
                   + f'<text class="chip" x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle">{name}'
                   + anim("fill", [t["text"], t["text"], t["bg1"], t["bg1"], t["text"], t["text"]], [0, tk, tk + .02, .92, .95, 1], D) + '</text>')
        cxl, cyl = cols[c] + 6, 130 + 36 * used[c]
        used[c] += 1
        out.append(f'<g opacity="0">' + anim("opacity", [0, 0, 1, 1, 0, 0], [0, tk + .02, tk + .05, .92, .95, 1], D)
                   + f'<rect x="{cxl}" y="{cyl}" width="62" height="28" rx="6" fill="{colors[c]}"/>'
                   + f'<text class="chip" x="{cxl + 31}" y="{cyl + 18}" text-anchor="middle" style="fill:{t["bg1"]}">{name}</text></g>')
    out.append(f'<text class="small" x="449" y="228" text-anchor="middle" style="fill:{t["ok"]}" opacity="0">0 clashes'
               + anim("opacity", [0, 0, 1, 1, 0, 0], [0, .6, .63, .92, .95, 1], D) + '</text>')
    return "".join(out)


def cards(t):
    food, g, h = body_foodbridge(t)
    return {
        "safetrail": card(t, "SafeTrail", "An SOS that survives no signal · FastAPI, React PWA",
                          body_safetrail(t), "saved offline, delivered on reconnect · no SOS step waits on the AI",
                          pill="1ST PLACE · BIOS 2026"),
        "cricket": card(t, "Cricket lakehouse", "Ball-by-ball JSON to gold tables, exactly once",
                        body_cricket(t), "8,852 real matches · 2,026,949 balls · 19/19 checks pass",
                        tag="PySpark · Delta Lake"),
        "foodbridge": card(t, "FoodBridge", "Why the matcher solves the whole board at once", food,
                           f"same 4×4 scores: greedy {g:.2f} → Hungarian {h:.2f} (+{(h / g - 1) * 100:.0f}%)",
                           tag="FastAPI · PostGIS"),
        "timetable": card(t, "Timetable generator", "Classes are vertices, clashes are edges, slots are colours",
                          body_timetable(t), "example: 6 classes, 3 slots, 0 clashes · backtracking + annealing",
                          tag="Java · JavaFX"),
    }


def main():
    OUT.mkdir(exist_ok=True)
    token = os.environ.get("GITHUB_TOKEN")
    stats = fetch_stats(token) if token else None
    for mode, theme in THEMES.items():
        (OUT / f"header-{mode}.svg").write_text(header_svg(theme), encoding="utf-8")
        if stats:
            (OUT / f"stats-{mode}.svg").write_text(stats_svg(theme, stats), encoding="utf-8")
        for name, svg in cards(theme).items():
            (OUT / f"card-{name}-{mode}.svg").write_text(svg, encoding="utf-8")
    print("header and cards written" + (f"; stats: {stats['repos']} repos" if stats else "; no GITHUB_TOKEN, stats skipped"))


if __name__ == "__main__":
    main()
