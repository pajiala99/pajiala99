"""Draw the three contact badges under the profile header (Portfolio, LinkedIn, Email).

They copy the look of shields.io's for-the-badge style, which forces all text to capitals and so showed
the email as HARDIKPAJIALA@GMAIL.COM. Here the labels stay in capitals and the values keep their real case.
Run locally on a Mac when a contact detail changes (it measures text with the system's Verdana):
    python3 scripts/build_badges.py
The daily workflow doesn't run this; the badges are static. Bump ?v=N on the README links after a change.
Logos: Simple Icons (GitHub Pages, Gmail) and Font Awesome (LinkedIn), as packaged by react-icons.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets"
VERDANA = "/System/Library/Fonts/Supplemental/Verdana.ttf"
VERDANA_BOLD = "/System/Library/Fonts/Supplemental/Verdana Bold.ttf"
H, SIZE, LOGO = 28, 10, 14          # shields for-the-badge: 28 px tall, 10 px text, 14 px logo
LABEL_BG = "#555"
LABEL_TRACK, VALUE_TRACK = 1.25, 0.6  # extra px between letters

LOGOS = {
    "githubpages": {
        "viewBox": "0 0 24 24",
        "paths": [
            "M14.088 13.126h-.296V9.858h.998c.815 0 1.094.47 1.094.98s-.28.98-1.094.98h-.701v1.308zm0-1.582h.74a.642.642 0 0 0 .733-.705.642.642 0 0 0-.732-.706h-.741zm2.881-.37a1.913 1.913 0 0 0-.653.11v-.262a1.756 1.756 0 0 1 .653-.118c.654 0 .824.297.824.732v1.49h-.17l-.066-.174a1.143 1.143 0 0 1-.657.218.663.663 0 0 1-.763-.702c0-.37.205-.645.776-.68l.575-.035v-.122c0-.318-.113-.457-.519-.457zm-.078.85c-.31.03-.445.192-.445.445 0 .196.048.431.462.431a1.056 1.056 0 0 0 .58-.174v-.758zm1.86.493a.252.252 0 0 0-.083.16c0 .11.053.158.166.17l.74.088c.41.044.598.205.598.584 0 .532-.532.74-1.133.74-.61 0-.976-.178-.976-.657a.609.609 0 0 1 .449-.575v-.005a.321.321 0 0 1-.14-.287.392.392 0 0 1 .166-.297.746.746 0 0 1-.349-.714c0-.449.192-.82.85-.82a1.36 1.36 0 0 1 .349.044h.74v.165l-.365.105a.908.908 0 0 1 .126.505c0 .449-.192.82-.85.82a1.397 1.397 0 0 1-.288-.027zm.127.588c-.288.065-.532.2-.532.48 0 .322.244.413.693.413.435 0 .845-.109.845-.48 0-.221-.105-.309-.37-.34zm.727-1.381c0-.288-.056-.554-.566-.554-.51 0-.567.266-.567.554 0 .288.057.553.567.553.51 0 .566-.266.566-.554zm1.637-.82c.74 0 .828.506.828 1.133v.14h-1.438c.018.379.118.723.61.723a1.665 1.665 0 0 0 .719-.122v.261a1.765 1.765 0 0 1-.719.131c-.736 0-.915-.505-.915-1.133s.179-1.133.915-1.133zm-.61 1.024h1.133c0-.387-.022-.753-.523-.753-.506 0-.597.36-.61.753zm2.601-.052c.619.057.767.266.767.623 0 .336-.213.671-.876.671a2.147 2.147 0 0 1-.649-.109V12.8a1.924 1.924 0 0 0 .654.1c.453 0 .575-.192.575-.397 0-.2-.061-.34-.492-.374-.632-.057-.763-.28-.763-.58 0-.31.2-.645.815-.645a1.627 1.627 0 0 1 .627.11v.26a1.799 1.799 0 0 0-.631-.1c-.432 0-.523.162-.523.376 0 .19.078.29.496.326zm-20.787-.659H1.38a.05.05 0 0 0-.05.05v.522a.05.05 0 0 0 .05.05h.416v.649a1.267 1.267 0 0 1-.351.032c-.305 0-.731-.112-.731-1.048s.443-1.06.86-1.06a1.69 1.69 0 0 1 .614.094.05.05 0 0 0 .06-.05l.12-.504a.047.047 0 0 0-.02-.039 1.715 1.715 0 0 0-.903-.165C.73 9.748 0 10.05 0 11.508s.837 1.675 1.542 1.675a1.736 1.736 0 0 0 .938-.25.043.043 0 0 0 .016-.038v-1.628a.05.05 0 0 0-.05-.05zm5.545-1.294a.05.05 0 0 0-.05-.05H7.34a.05.05 0 0 0-.05.05v1.161h-.936V9.923a.05.05 0 0 0-.05-.05h-.6a.05.05 0 0 0-.05.05v3.145a.05.05 0 0 0 .05.05h.6a.05.05 0 0 0 .05-.05v-1.345h.937l-.002 1.345a.05.05 0 0 0 .05.05h.603a.05.05 0 0 0 .05-.05zm-4.389.412a.388.388 0 1 0-.387.392.39.39 0 0 0 .387-.392zm-.042 2.068v-1.451a.05.05 0 0 0-.05-.05h-.6a.057.057 0 0 0-.051.056v2.08c0 .06.038.079.087.079h.54c.06 0 .074-.03.074-.08zm6.764-1.497h-.597a.05.05 0 0 0-.05.05v1.542a.673.673 0 0 1-.367.11c-.215 0-.272-.097-.272-.307v-1.344a.05.05 0 0 0-.05-.05h-.604a.05.05 0 0 0-.05.05v1.446c0 .626.348.779.828.779a1.398 1.398 0 0 0 .71-.217 1.274 1.274 0 0 0 .022.128.052.052 0 0 0 .044.027l.385-.002a.05.05 0 0 0 .05-.05v-2.112a.05.05 0 0 0-.05-.05zm1.662-.07a1.121 1.121 0 0 0-.569.15V9.923a.05.05 0 0 0-.05-.05h-.602a.05.05 0 0 0-.05.05v3.145a.05.05 0 0 0 .05.05h.418a.05.05 0 0 0 .044-.027.973.973 0 0 0 .025-.144 1.08 1.08 0 0 0 .713.233c.548 0 .862-.278.862-1.248s-.502-1.095-.841-1.095zm-.235 1.771a.716.716 0 0 1-.347-.1v-.996a.793.793 0 0 1 .308-.1c.215-.019.422.046.422.558 0 .54-.094.647-.383.639zm-6.475-1.706h-.45l-.002-.595c0-.023-.011-.034-.037-.034h-.615c-.024 0-.036.01-.036.033v.615l-.33.08a.05.05 0 0 0-.035.048v.387a.05.05 0 0 0 .05.05h.315v.93c0 .692.484.76.812.76a1.375 1.375 0 0 0 .357-.06.046.046 0 0 0 .028-.044l.001-.426a.05.05 0 0 0-.05-.05c-.026 0-.094.01-.163.01-.221 0-.296-.102-.296-.236v-.884h.451a.05.05 0 0 0 .05-.05v-.484a.05.05 0 0 0-.05-.05z"
        ]
    },
    "linkedin": {
        "viewBox": "0 0 448 512",
        "paths": [
            "M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"
        ]
    },
    "gmail": {
        "viewBox": "0 0 24 24",
        "paths": [
            "M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"
        ]
    }
}

BADGES = [
    ("portfolio", "PORTFOLIO", "pajiala99.github.io", "#d4a94c", "githubpages"),
    ("linkedin", "LINKEDIN", "hardik-pajiala", "#0A66C2", "linkedin"),
    ("email", "EMAIL", "hardikpajiala@gmail.com", "#555", "gmail"),
]


def width(text, path, track):
    """Rendered width in px at SIZE, with the tracking the badge adds between letters."""
    font = ImageFont.truetype(path, SIZE * 20)
    return font.getlength(text) / 20 + track * (len(text) - 1)


def badge(label, value, color, logo):
    lw_text, vw_text = width(label, VERDANA, LABEL_TRACK), width(value, VERDANA_BOLD, VALUE_TRACK)
    label_w = round(9 + LOGO + 6 + lw_text + 12)
    value_w = round(12 + vw_text + 12)
    w = label_w + value_w
    icon = LOGOS[logo]
    paths = "".join(f'<path d="{d}"/>' for d in icon["paths"])
    title = escape(f"{label.title()}: {value}")
    # textLength pins each text to its measured width, so a viewer without Verdana still fits the box
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" role="img" aria-label="{title}">'
        f"<title>{title}</title>"
        f'<g shape-rendering="crispEdges"><rect width="{label_w}" height="{H}" fill="{LABEL_BG}"/>'
        f'<rect x="{label_w}" width="{value_w}" height="{H}" fill="{color}"/></g>'
        f'<svg x="9" y="{(H - LOGO) / 2}" width="{LOGO}" height="{LOGO}" viewBox="{icon["viewBox"]}" fill="#fff">{paths}</svg>'
        f'<g fill="#fff" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="{SIZE}" text-rendering="geometricPrecision">'
        f'<text x="{9 + LOGO + 6}" y="17.5" textLength="{lw_text:.1f}">{escape(label)}</text>'
        f'<text x="{label_w + 12}" y="17.5" textLength="{vw_text:.1f}" font-weight="bold">{escape(value)}</text>'
        "</g></svg>\n"
    )


def main():
    for name, label, value, color, logo in BADGES:
        svg = badge(label, value, color, logo)
        (OUT / f"badge-{name}.svg").write_text(svg)
        print(f"  badge-{name}.svg")


if __name__ == "__main__":
    main()
