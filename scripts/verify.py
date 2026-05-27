
# AI GENERATED FILE: needs review and refactor

import os
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))

SVG_DIR = os.path.join(ROOT, "resources/icons")
DRAWABLE_DIR = os.path.join(ROOT, "app/src/main/res/drawable-nodpi")

APPFILTER = os.path.join(ROOT, "app/src/main/res/xml/appfilter.xml")
DRAWABLE_XML = os.path.join(ROOT, "app/src/main/res/xml/drawable.xml")

IGNORE_FILE = os.path.join(ROOT, "scripts/ignore.txt")

LOG_DIR = os.path.join(ROOT, "scripts/logs")
os.makedirs(LOG_DIR, exist_ok=True)


# ---------- IGNORE ----------
def load_ignore():
    if not os.path.exists(IGNORE_FILE):
        return set()
    with open(IGNORE_FILE, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


# ---------- SOURCES ----------
def list_svgs():
    return {f[:-4] for f in os.listdir(SVG_DIR) if f.endswith(".svg")}


def list_drawables():
    return {os.path.splitext(f)[0] for f in os.listdir(DRAWABLE_DIR) if f.endswith(".png")}


def parse_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return {i.attrib.get("drawable") for i in root.findall(".//item") if i.attrib.get("drawable")}


# ---------- LOG ----------
def log(text):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(LOG_DIR, f"verify_{ts}.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[verify] saved: {path}")


# ---------- MAIN ----------
def main():
    ignore = load_ignore()

    svgs = list_svgs() - ignore
    pngs = list_drawables() - ignore
    xml_drawable = parse_xml(DRAWABLE_XML) - ignore
    appfilter = parse_xml(APPFILTER) - ignore

    # --- core diff logic ---
    missing_png = svgs - pngs
    orphan_png = pngs - svgs

    missing_xml = pngs - xml_drawable
    orphan_xml = xml_drawable - pngs

    missing_appfilter = xml_drawable - appfilter
    orphan_appfilter = appfilter - xml_drawable

    # --- report ---
    r = []
    r.append("=== VERIFY REPORT ===\n")

    r.append(f"SVG: {len(svgs)}")
    r.append(f"PNG: {len(pngs)}")
    r.append(f"DRAWABLE XML: {len(xml_drawable)}")
    r.append(f"APPFILTER: {len(appfilter)}\n")

    def block(title, data):
        r.append(title)
        if data:
            for i in sorted(data):
                r.append(f"- {i}")
        else:
            r.append("- OK")
        r.append("")

    block("MISSING PNG (SVG → PNG):", missing_png)
    block("ORPHAN PNG:", orphan_png)

    block("MISSING DRAWABLE XML:", missing_xml)
    block("ORPHAN DRAWABLE XML:", orphan_xml)

    block("MISSING APPFILTER:", missing_appfilter)
    block("ORPHAN APPFILTER:", orphan_appfilter)

    log("\n".join(r))


if __name__ == "__main__":
    main()