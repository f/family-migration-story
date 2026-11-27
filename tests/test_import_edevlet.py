# Regression tests for scripts/import_edevlet.py, on synthetic e-Devlet PDFs (see edevlet_fixture.py).
#
# usage:
#   uv run --python 3.12 --with pypdf --with reportlab python -I tests/test_import_edevlet.py
#   IMPORTER=/path/to/other/import_edevlet.py uv run ... python -I tests/test_import_edevlet.py
#
# Two PDFs are built: a clean one, and one with the browser's print header/footer on every page
# (timestamp, page title, URL, page counter) at the positions a real "Print > Save as PDF" puts them.
# Each test_* function is independent and pytest can collect them too; run directly, the file runs
# them all, prints every failure and exits 1 if any failed.
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edevlet_fixture as fx  # noqa: E402

IMPORTER = os.environ.get("IMPORTER") or os.path.join(
    HERE, "..", "skills", "family-migration-story", "scripts", "import_edevlet.py")

# What the importer must produce for the fictional family, by id (id = relation path from the subject).
EXPECTED = {
    "pFFF": dict(relation="Babasının Babasının Babası", given="Ali", surname="Örnek", sex="M", birth=("1895", True, "Selanik"),
                 living=False, death=("1961-11-12", "Ölüm 12/11/1961"), father_name="Hüseyin", mother_name="Hatice",
                 registry=("İzmir", "Karşıyaka Merkez", "Bostanlı Köyü", "12-34-1"), marital="Evli", father=None, mother=None),
    "pFFM": dict(relation="Babasının Babasının Annesi", given="Emine", surname="Örnek", sex="F", birth=("1900", True, "Selanik"),
                 living=False, death=("1975-02-03", "Ölüm 03/02/1975"), father_name="İsmail", mother_name="Şerife",
                 registry=("İzmir", "Karşıyaka Merkez", "Bostanlı Köyü", "12-34-2"), marital="Dul", father=None, mother=None),
    "pFF": dict(relation="Babasının Babası", given="Hasan", surname="Örnek", sex="M", birth=("1925", True, "İzmir"),
                living=False, death=("1998-01-07", "Ölüm 07/01/1998"), father_name="Ali", mother_name="Emine",
                registry=("İzmir", "Karşıyaka Merkez", "Bostanlı Köyü", "12-34-3"), marital="Evli", father="pFFF", mother="pFFM"),
    "pFM": dict(relation="Babasının Annesi", given="Fatma", surname="Örnek", sex="F", birth=("1930", True, "İzmir"),
                living=False, death=("2010-05-30", "Ölüm 30/05/2010"), father_name="Osman", mother_name="Gülsüm",
                registry=("İzmir", "Karşıyaka Merkez", "Bostanlı Köyü", "12-34-4"), marital="Dul", father=None, mother=None),
    "pMF": dict(relation="Annesinin Babası", given="Mehmet", surname="Yılmaz", sex="M", birth=("1935", True, "Of"),
                living=False, death=("2004-08-21", "Ölüm 21/08/2004"), father_name="Rıza", mother_name="Nazife",
                registry=("Trabzon", "Of Merkez", "Söğütlü Köyü", "45-67-1"), marital="Evli", father=None, mother=None),
    "pMM": dict(relation="Annesinin Annesi", given="Zehra", surname="Yılmaz", sex="F", birth=("1938", True, "Of"),
                living=False, death=("2015-12-09", "Ölüm 09/12/2015"), father_name="Şükrü", mother_name="Dürdane",
                registry=("Trabzon", "Of Merkez", "Söğütlü Köyü", "45-67-2"), marital="Dul", father=None, mother=None),
    "pF": dict(relation="Babası", given="Murat", surname="Örnek", sex="M", birth=("1960-09-02", False, "İzmir"),
               living=True, death=None, father_name="Hasan", mother_name="Fatma",
               registry=("İzmir", "Karşıyaka Merkez", "Bostanlı Köyü", "12-34-5"), marital="Evli", father="pFF", mother="pFM"),
    "pM": dict(relation="Annesi", given="Ayşe", surname="Örnek", sex="F", birth=("1964-03-18", False, "Of"),
               living=True, death=None, father_name="Mehmet", mother_name="Zehra",
               registry=("İzmir", "Karşıyaka Merkez", "Bostanlı Köyü", "12-34-6"), marital="Evli", father="pMF", mother="pMM"),
    "p0": dict(relation="Kendisi", given="Deniz", surname="Örnek", sex="F", birth=("1992-04-11", False, "Kadıköy"),
               living=True, death=None, father_name="Murat", mother_name="Ayşe",
               registry=("İzmir", "Karşıyaka Merkez", "Bostanlı Köyü", "12-34-7"), marital="Bekar", father="pF", mother="pM"),
}

# Browser print margins that must never end up in a field.
URL_OR_HEADER = re.compile(r"http|turkiye\.gov\.tr|Sorgulama|\d{1,2}:\d{2}\s?[AP]M|\b[AP]M\b|\d{1,2}\.\d{1,2}\.\d{4}\s+\d{1,2}:\d{2}")
PAGE_COUNTER = re.compile(r"(^|\s)\d+\s?/\s?\d+($|\s)|(^|\s)/(\s|$)")

_cache = {}


def imported(printed):
    """Build the fixture PDF (once per variant), run the importer on it, return the parsed JSON."""
    if printed not in _cache:
        tmp = _cache.setdefault("dir", tempfile.mkdtemp(prefix="edevlet-test-"))
        name = "soyagaci-yazdirilmis" if printed else "soyagaci"
        try:
            fx.find_font()
        except fx.FontMissing as e:
            if "pytest" in sys.modules:
                sys.modules["pytest"].skip(str(e))
            raise
        pdf = fx.build(os.path.join(tmp, name + ".pdf"), printed=printed)
        out = os.path.join(tmp, name + ".json")
        r = subprocess.run([sys.executable, "-I", IMPORTER, pdf, out], capture_output=True, text=True)
        if r.returncode != 0:
            raise AssertionError(f"importer failed on {name}.pdf:\n{r.stderr}")
        _cache[printed] = json.load(open(out, encoding="utf-8"))
    return _cache[printed]


def strings(o, path=""):
    """Every string in the tree with its JSON path."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def compare(tree, fields):
    """Differences between the imported people and EXPECTED, limited to the given field groups."""
    errors = []
    people = {p["id"]: p for p in tree["people"]}
    if "people" in fields:
        if len(tree["people"]) != len(EXPECTED):
            errors.append(f"expected {len(EXPECTED)} people, got {len(tree['people'])}")
        if set(people) != set(EXPECTED):
            errors.append(f"ids differ: missing {sorted(set(EXPECTED) - set(people))}, extra {sorted(set(people) - set(EXPECTED))}")
        if tree["review"]:
            errors.append(f"review is not empty: {tree['review']}")
    for pid, e in EXPECTED.items():
        p = people.get(pid)
        if not p:
            continue
        got = {}
        if "names" in fields:
            got.update(relation=p["relation"], given=p["given"], surname=p["surname"], sex=p["sex"],
                       father_name=p["father_name"], mother_name=p["mother_name"], father=p["father"], mother=p["mother"])
        if "birth" in fields:
            b = p["birth"]
            got["birth"] = (b["date"], b["date_is_year_only"], b["place"])
        if "status" in fields:
            got["living"] = p["living"]
            got["death"] = None if p["death"] is None else (p["death"]["date"], p["death"]["recorded"])
        if "registry" in fields:
            r = p["registry"]
            got.update(registry=(r["province"], r["district"], r["locality"], r["cilt_hane_bsn"]), marital=p["marital"])
        for k, v in got.items():
            if v != e[k]:
                errors.append(f"{pid}.{k}: expected {e[k]!r}, got {v!r}")
    return errors


def leaks(tree, pattern):
    return [f"{path} = {s!r}" for path, s in strings(tree["people"], "people") if pattern.search(s)]


def check(errors, what):
    if errors:
        raise AssertionError(what + ":\n  " + "\n  ".join(errors))


ALL = ("people", "names", "birth", "status", "registry")


def test_clean_pdf_parses_exactly():
    check(compare(imported(False), ALL), "clean PDF")


def test_printed_pdf_has_no_url_title_or_timestamp():
    # the original bug: the footer URL was glued in front of the given name on the second page
    tree = imported(True)
    check(leaks(tree, URL_OR_HEADER) + compare(tree, ("people", "names")), "printed PDF, URL/title/timestamp")


def test_printed_pdf_has_no_page_counter():
    # the counter ("2", "/", "2") comes out as three runs, next to the status column
    tree = imported(True)
    check(leaks(tree, PAGE_COUNTER) + compare(tree, ("status",)), "printed PDF, page counter")


def test_printed_pdf_parses_like_clean():
    tree = imported(True)
    check(compare(tree, ALL) + leaks(tree, URL_OR_HEADER) + leaks(tree, PAGE_COUNTER), "printed PDF, all fields")


def main():
    print(f"importer: {os.path.abspath(IMPORTER)}")
    try:
        fx.find_font()
    except fx.FontMissing as e:
        print(f"SKIP: {e}")
        return 0
    tests = [(n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)]
    failed = 0
    for name, f in tests:
        try:
            f()
            print(f"PASS {name}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}\n  {e}")
    print(f"{len(tests) - failed}/{len(tests)} passed" + (f" (PDFs in {_cache['dir']})" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
