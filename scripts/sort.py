# AI GENERATED FILE: needs review and refactor

import os
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))

DRAWABLE_XML = os.path.join(ROOT, "app/src/main/res/xml/drawable.xml")
LOG_DIR = os.path.join(ROOT, "scripts/logs")
os.makedirs(LOG_DIR, exist_ok=True)

APP_PREFIX = "app_"
SYS_PREFIX = "sys_"


def parse(path):
    tree = ET.parse(path)
    return tree, tree.getroot()


# fix: rebuild drawable.xml categories from scratch

def sort_drawable_xml():
    tree, root = parse(DRAWABLE_XML)

    app_icons = []
    sys_icons = []

    # Collect all drawable names
    for item in root.findall(".//item"):
        drawable = item.get("drawable")

        if not drawable:
            continue





        if drawable.startswith(SYS_PREFIX):
            sys_icons.append(drawable)
        else:
            app_icons.append(drawable)

    app_icons.sort()
    sys_icons.sort()

    for category in root.findall("category"):
        root.remove(category)

    app_cat = ET.SubElement(root, "category", {"title": "App Icons"})
    sys_cat = ET.SubElement(root, "category", {"title": "System Icons"})

    for drawable in app_icons:
        ET.SubElement(app_cat, "item", {"drawable": drawable})

    for drawable in sys_icons:
        ET.SubElement(sys_cat, "item", {"drawable": drawable})

    indent(root)
    tree.write(
        DRAWABLE_XML,
        encoding="utf-8",
        xml_declaration=True
    )

    return len(app_icons), len(sys_icons)


def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(LOG_DIR, f"sort_{ts}.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write(msg)
    print(f"[sort] log saved: {path}")


def main():
    app_count, sys_count = sort_drawable_xml()

    log(f"""=== SORT REPORT ===
drawable.xml sorted safely

App icons: {app_count}
System icons: {sys_count}
""")

    print("DONE: drawable.xml sorted safely")


if __name__ == "__main__":
    main()