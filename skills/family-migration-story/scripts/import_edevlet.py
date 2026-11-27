# Turn a Turkish e-Devlet "Alt-Üst Soy Bilgisi" PDF into familytree.json (local only, nothing is uploaded).
#
# usage: uv run --with pypdf python -I import_edevlet.py soyagaci.pdf familytree.json
#
# The PDF is a table. pypdf reports every text run with its page position, so each run is placed in a
# column by its horizontal centre and in a row by the nearest "Sıra" number. The "Yakınlık Derecesi"
# chain (e.g. "Babasının Annesinin Babası") gives each person's path from the subject, which is enough
# to rebuild the tree without guessing from names.
import json, re, sys
from datetime import date

import pypdf

COLS = ["sira", "sex", "rel", "given", "surname", "father", "mother", "birth", "registry", "cilt", "marital", "status"]
HEAD = {"Sıra": "sira", "C": "sex", "Yakınlık Derecesi": "rel", "Adı": "given", "Soyadı": "surname",
        "Baba Adı": "father", "Ana Adı": "mother", "Doğum Yeri ve": "birth", "İl-İlçe-Mahalle/": "registry",
        "Cilt-Hane-": "cilt", "Medeni": "marital", "Durumu": "status"}
STEP = {"babasının": "F", "babası": "F", "annesinin": "M", "annesi": "M", "oğlunun": "S", "oğlu": "S",
        "kızının": "D", "kızı": "D", "kendisi": ""}
DATE = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")
# A PDF saved with the browser's "Print" carries the browser's header (date-time, page title) and footer
# (URL, page counter) on every page. They sit outside the table but can still be assigned to a cell:
# the URL ended up in front of a given name. Table dates never carry a time, so the timestamp pattern
# ("11/27/26, 1:18 PM", "27.11.2026 13:18") cannot match a cell.
PRINT_MARGIN = re.compile(
    r"^(https?://\S+"
    r"|\d{1,2}[./]\d{1,2}[./]\d{2,4},?\s+\d{1,2}:\d{2}(\s?[AP]M)?"
    r"|\d+\s?/\s?\d+"
    r"|.* - Alt-Üst Soy Bilgisi Sorgulama)$", re.I)


def head_key(t):
    """Column for a header run. Header text is split differently between PDF versions
    ("İl-İlçe-Mahalle/" + "Köy" or one run "İl-İlçe-Mahalle/Köy"), so match by prefix too."""
    if t in HEAD:
        return HEAD[t]
    if t.startswith("İl-İlçe-Mahalle"):
        return "registry"
    if t.startswith("Doğum Yeri"):
        return "birth"
    return None


def tr_title(s):
    """Title-case with Turkish dotted/dotless i rules (str.title() turns İZMİR into 'İzmi̇r')."""
    if not s:
        return s
    low = s.replace("I", "ı").replace("İ", "i").lower()
    return re.sub(r"(^|[\s/(-])(\w)", lambda m: m.group(1) + {"i": "İ", "ı": "I"}.get(m.group(2), m.group(2).upper()), low)


def width(t, fs):
    return len(t) * fs * 0.52


def runs(page):
    out = []
    def v(text, cm, tm, fd, fs):
        t = text.strip()
        if t:
            size = fs * (abs(tm[0]) or 1)
            out.append({"x": tm[4], "y": tm[5], "cx": tm[4] + width(t, size) / 2, "t": t})
    page.extract_text(visitor_text=v)
    # Drop the print margins: every run on the line of a recognised header/footer run, because the
    # browser draws the page counter as separate runs ("2", "/", "5") that are meaningless alone.
    margin_y = {round(r["y"]) for r in out if PRINT_MARGIN.match(r["t"])}
    return [r for r in out if round(r["y"]) not in margin_y]


def parse_date(s):
    m = DATE.match(s or "")
    if not m:
        return None
    d, mo, y = m.groups()
    # The registry writes 01/07 when only the year is known.
    return y if (d, mo) == ("01", "07") else f"{y}-{mo}-{d}"


def main(pdf, out_path):
    reader = pypdf.PdfReader(pdf)
    centres, rows = None, []
    for page in reader.pages:
        rs = runs(page)
        heads = {head_key(r["t"]): r["cx"] for r in rs if head_key(r["t"])}
        if len(heads) >= 10:
            centres = heads
        if not centres:
            continue
        anchors = [r for r in rs if re.fullmatch(r"\d{1,3}", r["t"]) and abs(r["cx"] - centres["sira"]) < 25]
        if not anchors:
            continue
        top = min(a["y"] for a in anchors) - 80
        # the notes block ("AÇIKLAMALAR 1-) İŞBU BELGE ...") after the last row is not part of the table
        notes = [r["y"] for r in rs if r["t"].upper().startswith("AÇIKLAMALAR")]
        bottom = min(notes) if notes else float("inf")
        cells = [dict() for _ in anchors]
        for r in rs:
            if r in anchors or r["y"] < top or r["y"] >= bottom or head_key(r["t"]) or r["t"] in ("Tarihi", "Köy", "Birey Sıra No", "Hali"):
                continue
            col = min(centres, key=lambda c: abs(centres[c] - r["cx"]))
            if col == "sira" or abs(centres[col] - r["cx"]) > 120:
                continue
            k = min(range(len(anchors)), key=lambda i: abs(anchors[i]["y"] - r["y"]))
            if abs(anchors[k]["y"] - r["y"]) > 75:
                continue
            cells[k].setdefault(col, []).append(r)
        for a, c in zip(anchors, cells):
            row = {"sira": int(a["t"])}
            for col, items in c.items():
                items.sort(key=lambda r: (round(r["y"]), r["x"]))
                row[col] = [r["t"] for r in items]
            rows.append(row)

    people, by_path, review = [], {}, []
    for row in sorted(rows, key=lambda r: r["sira"]):
        rel = " ".join(row.get("rel", []))
        steps = [STEP.get(w.lower()) for w in rel.split()]
        if any(s is None for s in steps):
            review.append(f'row {row["sira"]}: unknown relation "{rel}"')
            continue
        path = "".join(steps)
        val = lambda k: " ".join(row.get(k, [])).strip()
        birth = row.get("birth", [])
        bdate = next((parse_date(t) for t in birth if DATE.match(t)), None)
        bplace = " ".join(t for t in birth if not DATE.match(t)).strip() or None
        st = row.get("status", [])
        alive = bool(st) and st[0].lower().startswith("sağ")
        ddate = next((parse_date(t) for t in st if DATE.match(t)), None)
        reg = [t.rstrip("/") for t in row.get("registry", [])]
        cilt = val("cilt")
        p = {
            "id": "p" + (path or "0"),
            "path": path,
            "relation": rel,
            "given": tr_title(val("given")) if val("given") not in ("", "-") else None,
            "surname": tr_title(val("surname")) if val("surname") not in ("", "-") else None,
            "sex": {"E": "M", "K": "F"}.get(val("sex")),
            "birth": {"date": bdate, "date_is_year_only": bool(bdate) and len(bdate) == 4, "place": tr_title(bplace) if bplace else None},
            "death": None if alive else {"date": ddate, "recorded": " ".join(st)},
            "living": alive,
            "father_name": tr_title(val("father")) if val("father") not in ("", "-") else None,
            "mother_name": tr_title(val("mother")) if val("mother") not in ("", "-") else None,
            "registry": {"province": reg[0] if reg else None, "district": reg[1] if len(reg) > 1 else None,
                         "locality": tr_title(" ".join(reg[2:])) if len(reg) > 2 else None, "cilt_hane_bsn": cilt or None},
            "marital": val("marital") or None,
        }
        if not p["given"] or not bdate:
            review.append(f'{p["id"]}: missing given name or birth date')
        by_path[path] = p
        people.append(p)

    # parent links from the relation paths; descendants hang off their parent path
    for p in people:
        path = p["path"]
        p["father"] = by_path.get(path + "F", {}).get("id") if path + "F" in by_path else None
        p["mother"] = by_path.get(path + "M", {}).get("id") if path + "M" in by_path else None
    for p in people:
        path = p["path"]
        if path and path[-1] in "SD":
            parent = by_path.get(path[:-1])
            if parent:
                p["father" if parent["sex"] == "M" else "mother"] = parent["id"]
        p.pop("path")

    tree = {
        "subject": "p0",
        "source": {"type": "e-Devlet Alt-Üst Soy Belgesi", "file": pdf.split("/")[-1], "imported": date.today().isoformat()},
        "people": people,
        "events": [],
        "oral_history": [],
        "review": review,
    }
    json.dump(tree, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(people)} people -> {out_path}")
    for r in review:
        print("REVIEW", r)


if __name__ == "__main__":
    main(*sys.argv[1:3])
