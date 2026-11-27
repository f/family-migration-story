# Build a synthetic e-Devlet "Alt-Üst Soy Bilgisi" PDF for the import_edevlet.py tests.
#
# usage: uv run --with reportlab python -I edevlet_fixture.py out.pdf [--printed]
#
# The people are the fictional "Örnek ailesi" from assets/example/familytree.json. Only the layout
# comes from a real PDF that a browser saved with "Print": page size, the coordinate systems, column
# positions, row spacing, how multi-line cells are split into text runs and where the browser puts
# its header and footer. No name, date, place or number from a real document is in this file.
#
# The geometry matters because the importer reads raw text-matrix positions (pypdf's tm), not page
# positions. In a browser-printed PDF the table is drawn as one long page: its y keeps growing from
# page to page (the table header sits at y=245, 745, 1464, 2183 ...) and only the outer transform
# (cm) moves. The print header and footer are drawn in their own transform with y=30 and y=770 on
# every page. So on the second page the footer (y=770) lands 27 units above the first row (y=797),
# and the URL there used to be glued to that row's given name.
#
# Font: the table needs Turkish glyphs (İ ı ş ğ ö ü ç), which the PDF base fonts do not have. A TTF
# is looked up in EDEVLET_TEST_FONT, then DejaVu Sans (Linux), then Arial (macOS, Windows). Glyph
# widths do not matter to the importer (it estimates widths from the character count), so any font
# with Turkish glyphs gives the same result.
import os, sys

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


class FontMissing(RuntimeError):
    pass


def find_font():
    for path in [os.environ.get("EDEVLET_TEST_FONT")] + FONT_CANDIDATES:
        if path and os.path.isfile(path):
            return path
    raise FontMissing("no TTF with Turkish glyphs found; set EDEVLET_TEST_FONT=/path/to/font.ttf")


# ---- geometry measured on a real browser-printed PDF (A4 landscape) ----
PAGE = (841.92, 594.96)
SCALE = 0.75                    # CSS px -> pt
CONTENT_F0 = 567.21             # content transform: cm = [.75 0 0 -.75 27.75 567.21 + 539.25*page]
CONTENT_E = 27.75
PAGE_STEP = 719                 # CSS px per printed page (539.25 pt)
MARGIN_CM = (SCALE, 0, 0, -SCALE, 0, 594.96)   # print header/footer transform, the same on every page
SIZE, MARGIN_SIZE, TITLE_SIZE = 12, 10.66, 16
LINE = 18                       # line height inside a cell; a 2-line cell is at -9/+9, a 3-line one at -18/0/+18
ROW = 61                        # distance between rows
FIRST_HEADER, HEADER_TO_ROW = 245, 52
NEXT_HEADER = 26                # header y on later pages, + PAGE_STEP * page
PAGE_BOTTOM = 720               # a row whose cell box (anchor + 30) passes this goes to the next page

# Header runs: (text, x, dy from the header line). Two-line headers are two runs.
HEADER = [("Sıra", 34.97, 0), ("C", 64.50, 0), ("Yakınlık Derecesi", 92.27, 0), ("Adı", 239.52, 0),
          ("Soyadı", 312.30, 0), ("Baba Adı", 388.14, 0), ("Ana Adı", 481.77, 0),
          ("Doğum Yeri ve", 560.89, -9), ("Tarihi", 585.41, 9), ("İl-İlçe-Mahalle/Köy", 672.05, 0),
          ("Cilt-Hane-", 807.64, -9), ("Birey Sıra No", 799.22, 9), ("Medeni", 891.09, -9),
          ("Hali", 901.17, 9), ("Durumu", 958.59, 0)]
# Cell text is centred on these x positions (from the real runs' x plus half their width).
CENTRE = {"sira": 45.5, "sex": 68.5, "rel": 140.0, "given": 246.0, "surname": 331.0, "father": 410.0,
          "mother": 503.0, "birth": 602.0, "registry": 722.0, "cilt": 836.0, "marital": 914.5, "status": 982.5}
# Title block on the first page and the notes block after the last row.
TITLE = [("T.C.", 136), ("İÇİŞLERİ BAKANLIĞI", 160), ("NÜFUS VE VATANDAŞLIK İŞLERİ GENEL MÜDÜRLÜĞÜ", 184),
         ("ALT-ÜST SOY BİLGİSİ", 208)]
NOTES_GAP, NOTE_LINE_GAP = 43, 25
NOTE = "Bu belge yalnızca test için uydurma kişilerle üretilmiştir; gerçek bir nüfus kaydı değildir."
# Browser print header/footer (x, y in MARGIN_CM). The page counter is three runs: "2", "/", "2".
STAMP = "11/27/26, 1:18 PM"
PAGE_TITLE = "Nüfus ve Vatandaşlık İşleri Genel Müdürlüğü - Alt-Üst Soy Bilgisi Sorgulama"
URL = "https://www.turkiye.gov.tr/nvi-alt-ust-soy-bilgisi-sorgulama"

# ---- the fictional family (same people as assets/example/familytree.json) ----
# Rows are ordered as e-Devlet does: the oldest generation first, the subject ("Kendisi") last.
# date strings are DD/MM/YYYY as in the document; 01/07/YYYY means "only the year is known".
FAMILY = [
    dict(sex="E", rel="Babasının Babasının Babası", given="ALİ", surname="ÖRNEK", father="HÜSEYİN", mother="HATİCE",
         place="SELANİK", born="01/07/1895", registry=("İzmir/", "Karşıyaka Merkez/", "BOSTANLI KÖYÜ"),
         cilt="12-34-1", marital="Evli", death="12/11/1961"),
    dict(sex="K", rel="Babasının Babasının Annesi", given="EMİNE", surname="ÖRNEK", father="İSMAİL", mother="ŞERİFE",
         place="SELANİK", born="01/07/1900", registry=("İzmir/", "Karşıyaka Merkez/", "BOSTANLI KÖYÜ"),
         cilt="12-34-2", marital="Dul", death="03/02/1975"),
    dict(sex="E", rel="Babasının Babası", given="HASAN", surname="ÖRNEK", father="ALİ", mother="EMİNE",
         place="İZMİR", born="01/07/1925", registry=("İzmir/", "Karşıyaka Merkez/", "BOSTANLI KÖYÜ"),
         cilt="12-34-3", marital="Evli", death="07/01/1998"),
    dict(sex="K", rel="Babasının Annesi", given="FATMA", surname="ÖRNEK", father="OSMAN", mother="GÜLSÜM",
         place="İZMİR", born="01/07/1930", registry=("İzmir/", "Karşıyaka Merkez/", "BOSTANLI KÖYÜ"),
         cilt="12-34-4", marital="Dul", death="30/05/2010"),
    dict(sex="E", rel="Annesinin Babası", given="MEHMET", surname="YILMAZ", father="RIZA", mother="NAZİFE",
         place="OF", born="01/07/1935", registry=("Trabzon/", "Of Merkez/", "SÖĞÜTLÜ KÖYÜ"),
         cilt="45-67-1", marital="Evli", death="21/08/2004"),
    dict(sex="K", rel="Annesinin Annesi", given="ZEHRA", surname="YILMAZ", father="ŞÜKRÜ", mother="DÜRDANE",
         place="OF", born="01/07/1938", registry=("Trabzon/", "Of Merkez/", "SÖĞÜTLÜ KÖYÜ"),
         cilt="45-67-2", marital="Dul", death="09/12/2015"),
    dict(sex="E", rel="Babası", given="MURAT", surname="ÖRNEK", father="HASAN", mother="FATMA",
         place="İZMİR", born="02/09/1960", registry=("İzmir/", "Karşıyaka Merkez/", "BOSTANLI KÖYÜ"),
         cilt="12-34-5", marital="Evli", death=None),
    dict(sex="K", rel="Annesi", given="AYŞE", surname="ÖRNEK", father="MEHMET", mother="ZEHRA",
         place="OF", born="18/03/1964", registry=("İzmir/", "Karşıyaka Merkez/", "BOSTANLI KÖYÜ"),
         cilt="12-34-6", marital="Evli", death=None),
    dict(sex="K", rel="Kendisi", given="DENİZ", surname="ÖRNEK", father="MURAT", mother="AYŞE",
         place="KADIKÖY", born="11/04/1992", registry=("İzmir/", "Karşıyaka Merkez/", "BOSTANLI KÖYÜ"),
         cilt="12-34-7", marital="Bekar", death=None),
]


def lines(n):
    """y offsets of n lines centred on the row anchor: 1 -> [0], 2 -> [-9, 9], 3 -> [-18, 0, 18]."""
    return [LINE * i - LINE * (n - 1) / 2 for i in range(n)]


def cells(p):
    """Each column's text runs, split the way the browser wraps them: two relation words per line."""
    words = p["rel"].split()
    rel = [" ".join(words[i:i + 2]) for i in range(0, len(words), 2)]
    status = ["Sağ", "-"] if p["death"] is None else ["Ölüm", p["death"]]
    return {"sex": [p["sex"]], "rel": rel, "given": [p["given"]], "surname": [p["surname"]],
            "father": [p["father"]], "mother": [p["mother"]], "birth": [p["place"], p["born"]],
            "registry": list(p["registry"]), "cilt": [p["cilt"]], "marital": [p["marital"]], "status": status}


def layout(people):
    """Assign every row to a page and an anchor y. Returns [(page, header_y, [(sira, y, person)])]."""
    pages, y, page = [], FIRST_HEADER + HEADER_TO_ROW, 0
    pages.append((0, FIRST_HEADER, []))
    for i, p in enumerate(people, 1):
        if y + ROW / 2 > PAGE_STEP * page + PAGE_BOTTOM:
            page += 1
            header = NEXT_HEADER + PAGE_STEP * page
            pages.append((page, header, []))
            y = header + HEADER_TO_ROW
        pages[-1][2].append((i, y, p))
        y += ROW
    return pages


def build(out_path, printed=False, people=FAMILY, stamp=STAMP):
    """Write the synthetic PDF. printed=True adds the browser's print header and footer on every page."""
    font = find_font()
    pdfmetrics.registerFont(TTFont("TestTR", font))
    c = canvas.Canvas(out_path, pagesize=PAGE)
    pages = layout(people)
    # the notes block ("AÇIKLAMALAR ...") follows the last row on the last page
    notes_y = pages[-1][2][-1][1] + NOTES_GAP
    total = len(pages)

    def text(t, x, y, size=SIZE):
        # Tm = [1 0 0 -1 x y]: upright glyphs in the flipped content space, tm[4]/tm[5] = x/y as in the real PDF
        o = c.beginText()
        o.setFont("TestTR", size)
        o.setTextTransform(1, 0, 0, -1, x, y)
        o.textOut(t)
        c.drawText(o)

    def centred(t, col, y):
        text(t, CENTRE[col] - pdfmetrics.stringWidth(t, "TestTR", SIZE) / 2, y)

    for page, header_y, rows in pages:
        c.saveState()
        c.transform(SCALE, 0, 0, -SCALE, CONTENT_E, CONTENT_F0 + PAGE_STEP * SCALE * page)
        if page == 0:
            for t, y in TITLE:
                text(t, 540 - pdfmetrics.stringWidth(t, "TestTR", TITLE_SIZE) / 2, y, TITLE_SIZE)
        for t, x, dy in HEADER:
            text(t, x, header_y + dy)
        for sira, y, p in rows:
            centred(str(sira), "sira", y)
            for col, runs in cells(p).items():
                for t, dy in zip(runs, lines(len(runs))):
                    centred(t, col, y + dy)
        if page == pages[-1][0]:
            text("AÇIKLAMALAR", 34.00, notes_y)
            text("1-)", 38.73, notes_y + NOTE_LINE_GAP)
            text(NOTE, 64.02, notes_y + NOTE_LINE_GAP)
        c.restoreState()
        if printed:
            c.saveState()
            c.transform(*MARGIN_CM)
            text(stamp, 32.00, 30, MARGIN_SIZE)
            text(PAGE_TITLE, 454.47, 30, MARGIN_SIZE)
            text(URL, 32.00, 770, MARGIN_SIZE)
            # the page counter comes out of the browser as three separate runs
            text(str(page + 1), 1077.02, 770, MARGIN_SIZE)
            text("/", 1082.36, 770, MARGIN_SIZE)
            text(str(total), 1085.33, 770, MARGIN_SIZE)
            c.restoreState()
        c.showPage()
    c.save()
    return out_path


if __name__ == "__main__":
    build(sys.argv[1], printed="--printed" in sys.argv[2:])
    print(sys.argv[1])
