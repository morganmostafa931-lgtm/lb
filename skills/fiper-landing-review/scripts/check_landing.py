#!/usr/bin/env python3
"""Static checks for a Fiper landing page.

Usage: python3 check_landing.py index.html [more.html ...]
Exit code 1 if any ERROR was found.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_attrs = {}
        self.title = ""
        self.in_title = False
        self.metas = []
        self.h1 = 0
        self.imgs = []
        self.ids = set()
        self.hrefs = []
        self.styles = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.html_attrs = a
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "h1":
            self.h1 += 1
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a" and a.get("href", "").startswith("#"):
            self.hrefs.append(a["href"])
        elif tag == "style":
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_style:
            self.styles.append(data)


def check_css(css, src, out):
    # Drop :root { ... } blocks (tokens live there), then look for raw colors.
    body = re.sub(r":root[^{]*\{[^}]*\}", "", css)
    raw = re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)", body)
    if raw:
        out.append(("WARN", f"{src}: {len(raw)} hard-coded color(s) outside :root, e.g. {raw[0]} — use var(--fiper-*)"))
    phys = re.findall(r"(?<![-\w])(margin-left|margin-right|padding-left|padding-right|left|right|text-align:\s*(?:left|right))\s*:", body)
    if phys:
        out.append(("WARN", f"{src}: physical direction properties ({', '.join(sorted(set(phys)))}) — prefer logical *-inline-* for RTL"))


def check(path):
    out = []
    text = Path(path).read_text(encoding="utf-8")
    c = Collector()
    c.feed(text)

    lang, d = c.html_attrs.get("lang"), c.html_attrs.get("dir")
    if not lang:
        out.append(("ERROR", "<html> has no lang attribute"))
    if lang and lang.startswith("ar") and d != "rtl":
        out.append(("ERROR", 'Arabic page without dir="rtl"'))

    t = c.title.strip()
    if not t:
        out.append(("ERROR", "missing <title>"))
    elif len(t) > 60:
        out.append(("WARN", f"<title> is {len(t)} chars (max 60)"))

    names = {m.get("name") or m.get("property"): m.get("content", "") for m in c.metas}
    if "viewport" not in names:
        out.append(("ERROR", "missing <meta name=viewport>"))
    desc = names.get("description")
    if not desc:
        out.append(("ERROR", "missing meta description"))
    elif not 120 <= len(desc) <= 160:
        out.append(("WARN", f"meta description is {len(desc)} chars (aim 120-155)"))
    for og in ("og:title", "og:description", "og:image"):
        if og not in names:
            out.append(("WARN", f"missing {og}"))

    if c.h1 != 1:
        out.append(("ERROR", f"page has {c.h1} <h1> (expected exactly 1)"))

    for i, img in enumerate(c.imgs, 1):
        src = img.get("src", f"#{i}")
        if "alt" not in img:
            out.append(("ERROR", f"<img {src}> has no alt"))
        if not (img.get("width") and img.get("height")):
            out.append(("WARN", f"<img {src}> has no width/height (layout shift)"))

    for h in set(c.hrefs):
        if h != "#" and h[1:] not in c.ids:
            out.append(("ERROR", f"link {h} points to a missing id"))

    for css in c.styles:
        check_css(css, "<style>", out)
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\':]+)["\']', text):
        p = Path(path).parent / href
        if p.exists():
            check_css(p.read_text(encoding="utf-8"), href, out)

    todos = len(re.findall(r"TODO|\[placeholder\]", text))
    if todos:
        out.append(("WARN", f"{todos} TODO/[placeholder] left in the page"))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    failed = False
    for path in sys.argv[1:]:
        print(f"== {path}")
        results = check(path)
        for level, msg in results:
            print(f"  {level:5} {msg}")
            failed |= level == "ERROR"
        if not results:
            print("  OK    no issues found")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
