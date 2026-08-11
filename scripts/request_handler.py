#!/usr/bin/env python3

# AI GENERATED FILE: needs review

import argparse
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

REQUESTS_DIR = BASE_DIR / "requests"
ICONS_DIR = REQUESTS_DIR / "icons"
DB_FILE = REQUESTS_DIR / "requests_index.json"

APPFILTER_FILE = BASE_DIR / "app" / "src" / "main" / "res" / "xml" / "appfilter.xml"


def load_db() -> dict:
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text(encoding="utf-8"))

    return {}


def save_db(db: dict) -> None:
    REQUESTS_DIR.mkdir(parents=True, exist_ok=True)

    # Always keep sorted by popularity.
    sorted_db = dict(
        sorted(
            db.items(),
            key=lambda x: x[1].get("count", 0),
            reverse=True
        )
    )

    DB_FILE.write_text(
        json.dumps(sorted_db, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_appfilter_components() -> set[str]:
    """
    Returns all components already implemented
    in app/src/main/res/xml/appfilter.xml.
    """

    if not APPFILTER_FILE.exists():
        print(f"⚠ appfilter.xml not found: {APPFILTER_FILE}")
        return set()

    try:
        root = ET.parse(APPFILTER_FILE).getroot()
    except ET.ParseError as e:
        print(f"❌ Failed to parse appfilter.xml: {e}")
        return set()

    components = set()

    for item in root.iter("item"):
        component = item.attrib.get("component")

        if component:
            components.add(component)

    return components


def extract_xml(zip_path: str) -> str | None:
    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if "appfilter.xml" in name:
                return z.read(name).decode("utf-8")

    return None


def parse_appfilter(xml_text: str) -> list[dict]:
    lines = xml_text.splitlines()

    items = []
    last_comment = None

    for line in lines:
        line = line.strip()

        if line.startswith("<!--") and line.endswith("-->"):
            last_comment = (
                line
                .replace("<!--", "")
                .replace("-->", "")
                .strip()
            )
            continue

        if "<item" in line:
            try:
                elem = ET.fromstring(line)

                items.append({
                    "name": last_comment,
                    "component": elem.attrib.get("component"),
                    "drawable": elem.attrib.get("drawable")
                })

            except Exception:
                pass

            last_comment = None

    return items


def save_icon(zip_path: str, drawable: str | None) -> None:
    if not drawable:
        return

    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if name.endswith(".png") and drawable in name:
                out_file = ICONS_DIR / f"{drawable}.png"

                if not out_file.exists():
                    out_file.write_bytes(z.read(name))

                return


def process(
    zip_path: str,
    db: dict,
    implemented_components: set[str],
    ncount: bool = False
) -> dict:

    xml = extract_xml(zip_path)

    if not xml:
        print(f"❌ appfilter.xml not found in: {zip_path}")
        return db

    items = parse_appfilter(xml)

    unique = {}

    for item in items:
        component = item["component"]

        if component:
            unique[component] = item

    added = 0
    skipped = 0

    for key, item in unique.items():

        # Already implemented in the project's appfilter.xml.
        if key in implemented_components:
            skipped += 1
            continue

        # Init record.
        if key not in db:
            db[key] = {
                "name": item["name"] or "",
                "component": item["component"],
                "drawable": item["drawable"],
                "count": 0
            }

        # Update metadata.
        if item["name"]:
            db[key]["name"] = item["name"]

        db[key]["drawable"] = item["drawable"]

        if ncount:
            if db[key]["count"] == 0:
                db[key]["count"] = 1
        else:
            db[key]["count"] += 1

        save_icon(zip_path, item["drawable"])

        added += 1

    print(f"✔ Processed: {zip_path}")
    print(f"  Added/updated: {added}")

    if skipped:
        print(f"  Already implemented: {skipped}")

    return db


def check_requests(db: dict) -> dict:
    """
    Remove requests that are already implemented
    in the project's appfilter.xml.
    """

    implemented_components = load_appfilter_components()

    if not implemented_components:
        print("⚠ No implemented components found.")
        return db

    removed = []

    for component in list(db.keys()):
        if component in implemented_components:
            removed.append(component)
            del db[component]

    print(f"✔ Checked: {len(db) + len(removed)} requests")

    if removed:
        print(f"✔ Removed implemented requests: {len(removed)}")

        for component in removed:
            print(f"  - {component}")
    else:
        print("✔ Nothing to remove")

    return db


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Willow Icon Request Handler"
    )

    parser.add_argument(
        "zips",
        nargs="*",
        help="paths to request zip files"
    )

    parser.add_argument(
        "--ncount",
        action="store_true",
        help="do not increment counters, only ensure minimum presence"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="remove requests already implemented in appfilter.xml"
    )

    args = parser.parse_args()

    # --check works without ZIP files.
    if args.check:
        if args.zips:
            parser.error("--check cannot be used together with ZIP files")

        db = load_db()
        db = check_requests(db)
        save_db(db)

        print("✔ DB saved:", DB_FILE)

        return

    # Normal mode requires at least one ZIP.
    if not args.zips:
        parser.error("at least one ZIP file is required")

    db = load_db()

    # Read project's appfilter.xml once.
    implemented_components = load_appfilter_components()

    if implemented_components:
        print(
            f"✔ Found {len(implemented_components)} "
            f"implemented components in appfilter.xml"
        )

    for zip_path in args.zips:
        db = process(
            zip_path,
            db,
            implemented_components,
            ncount=args.ncount
        )

    save_db(db)

    print("✔ DB saved:", DB_FILE)
    print("✔ ICONS saved:", ICONS_DIR)


if __name__ == "__main__":
    main()