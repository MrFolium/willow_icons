
# AI GENERATED FILE: needs review and refactor

import os
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))

DRAWABLE_XML = os.path.join(ROOT, "app/src/main/res/xml/drawable.xml")
APPFILTER_XML = os.path.join(ROOT, "app/src/main/res/xml/appfilter.xml")

LOG_DIR = os.path.join(ROOT, "scripts/logs")
os.makedirs(LOG_DIR, exist_ok=True)


APP_PREFIX = "app_"
SYS_PREFIX = "sys_"


def indent(elem, level=0):
    """нормальный pretty print без каши"""
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


def parse(path):
    tree = ET.parse(path)
    return tree, tree.getroot()


def sort_drawable_xml():
    tree, root = parse(DRAWABLE_XML)

    items = [i for i in root.findall("item") if i.get("drawable")]

    apps = []
    sys = []

    for i in items:
        d = i.get("drawable")
        if d.startswith(SYS_PREFIX):
            sys.append(d)
        else:
            apps.append(d)

    apps.sort()
    sys.sort()

    # чистим XML
    for i in list(root):
        root.remove(i)

    # APP SECTION
    cat1 = ET.SubElement(root, "category", {"title": "App Icons"})
    for d in apps:
        ET.SubElement(cat1, "item", {"drawable": d})

    # SYS SECTION
    cat2 = ET.SubElement(root, "category", {"title": "System Icons"})
    for d in sys:
        ET.SubElement(cat2, "item", {"drawable": d})

    indent(root)

    tree.write(DRAWABLE_XML, encoding="utf-8", xml_declaration=True)

    return len(apps), len(sys)


def clean_empty_comments(xml_path):
    """убирает <!---->"""
    with open(xml_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        if "<!---->" in line:
            continue
        cleaned.append(line)

    with open(xml_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(LOG_DIR, f"sort_{ts}.log")
    with open(path, "w", encoding="utf-8") as f:
        f.write(msg)
    print(f"[sort] log saved: {path}")


def main():
    app_count, sys_count = sort_drawable_xml()

    clean_empty_comments(DRAWABLE_XML)

    log(f"""=== SORT REPORT ===
drawable.xml sorted

App icons: {app_count}
System icons: {sys_count}
""")

    print("DONE: drawable.xml sorted cleanly")


if __name__ == "__main__":
    main()