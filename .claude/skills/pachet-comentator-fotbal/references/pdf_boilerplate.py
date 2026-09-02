# -*- coding: utf-8 -*-
"""
Boilerplate testat pentru generarea pachetelor de comentator (stil Sky Sports Opta Facts).
Copiază și adaptează secțiunile de conținut; NU modifica partea de fonturi/stiluri
decât dacă știi ce faci — diacriticele românești depind de înregistrarea corectă
a fontului DejaVu Sans.

Rulează cu: pip install reportlab --break-system-packages (dacă nu e deja instalat)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import hashlib
import tempfile
import matplotlib
matplotlib.use("Agg")  # fără display — obligatoriu într-un mediu server/sandbox
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. FONTURI — obligatoriu pentru diacritice românești (ș, ț, ă, â, î)
# ---------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont('DejaVuSans', FONT_DIR + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', FONT_DIR + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold')

styles = getSampleStyleSheet()
for _sname in styles.byName:
    _s = styles[_sname]
    if not hasattr(_s, 'fontName'):
        continue
    if _s.fontName == 'Helvetica':
        _s.fontName = 'DejaVuSans'
    elif _s.fontName == 'Helvetica-Bold':
        _s.fontName = 'DejaVuSans-Bold'

# ---------------------------------------------------------------------------
# 2. CULORI — schimbă accent_color per echipă/club pentru identitate vizuală
# ---------------------------------------------------------------------------
accent_hex = "#c8102e"                       # aceeași culoare, ca string hex — matplotlib nu acceptă HexColor
accent_color = colors.HexColor(accent_hex)  # ex: roșu Forest / bleumarin OM / grena Nice
band = colors.HexColor("#dce8f5")           # fundal bară secțiune (deschis)
grey = colors.HexColor("#f2f2f2")           # rând alternant tabel
white_alt = colors.HexColor("#ffffff")
lightband = colors.HexColor("#f6eaea")      # fundal alternant pentru blocurile de loturi
muted_grey = "#9a9a9a"                       # serii/etichete neutre în grafice (nu evidențiate)

# ---------------------------------------------------------------------------
# 3. STILURI DE TEXT
# ---------------------------------------------------------------------------
title = ParagraphStyle('Title', parent=styles['Title'], fontSize=17, textColor=colors.black,
                        fontName='DejaVuSans-Bold', spaceAfter=2, alignment=0)
subtitle = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11,
                           textColor=colors.HexColor("#333333"), fontName='DejaVuSans-Bold', spaceAfter=10)
band_style = ParagraphStyle('Band', parent=styles['Normal'], fontSize=10.5, textColor=colors.black,
                             fontName='DejaVuSans-Bold')
sect = ParagraphStyle('Sect', parent=styles['Normal'], fontSize=9.5, textColor=accent_color,
                       fontName='DejaVuSans-Bold', spaceBefore=10, spaceAfter=4)
bullet = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=9, leading=12.5,
                         spaceAfter=5, leftIndent=10)
cell = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=8.3, leading=10.5)
cellb = ParagraphStyle('CellB', parent=styles['Normal'], fontSize=8.3, leading=10.5,
                        fontName='DejaVuSans-Bold')
compress = ParagraphStyle('Compress', parent=styles['Normal'], fontSize=7.6, leading=9.5)
foot = ParagraphStyle('Foot', parent=styles['Normal'], fontSize=7.5, textColor=colors.HexColor("#888888"))

# ---------------------------------------------------------------------------
# 4. HELPER-E
# ---------------------------------------------------------------------------
def band_bar(text):
    """Bară de secțiune pe toată lățimea paginii, stil Sky Sports."""
    t = Table([[Paragraph(text, band_style)]], colWidths=[17.2 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), band),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def two_col_table(rows, w1=8.6, w2=8.6, header_bg=None):
    """Tabel comparativ pe 2 coloane (ex: mercato IN/OUT, performanțe sezon trecut)."""
    header_bg = header_bg or accent_color
    t = Table(rows, colWidths=[w1 * cm, w2 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white_alt, grey]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


def simple_table(rows, col_widths_cm, header_bg=None):
    """Tabel generic (ex: cap la cap, absenți) cu header colorat."""
    header_bg = header_bg or accent_color
    t = Table(rows, colWidths=[w * cm for w in col_widths_cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white_alt, grey]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def squad_row_full(num, name, age, nat, height, career, stats):
    """Rând de jucător cu detalii complete (înălțime + carieră + statistici)."""
    txt = f"{num}. {name} - {age} ani - {nat}"
    if height:
        txt += f" - {height}"
    txt += f"<br/><b>Carieră:</b> {career}<br/><b>Sezonul trecut:</b> {stats}"
    return Paragraph(txt, compress)


def squad_row_simple(num, name, age, nat, note):
    """Rând de jucător în format scurt (fără carieră/statistici), stil Miro-block."""
    return Paragraph(f"{num}. {name} - {age} ani - {nat}<br/>{note}", compress)


def squad_block(story, title_text, players, row_fn=squad_row_simple):
    """Adaugă un grup de jucători (ex: 'Portari') ca tabel în story."""
    story.append(Paragraph(title_text, sect))
    rows = [[row_fn(*p)] for p in players]
    t = Table(rows, colWidths=[16.8 * cm])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white_alt, lightband]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 4))


def _chart_path(*parts):
    """Nume de fișier temporar stabil pentru un grafic, ca să nu aglomerăm /tmp cu duplicate."""
    key = hashlib.md5("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:12]
    return f"{tempfile.gettempdir()}/pachet_chart_{key}.png"


def bar_chart(labels, values, title="", highlight_label=None, value_fmt="{:.0f}",
              width_cm=16.8, height_cm=6.5):
    """Grafic bar orizontal simplu — ex: puncte per sezon, % dueluri câștigate pe toată liga.
    `highlight_label` (opțional) trebuie să fie identic cu unul din `labels`, ca să fie colorat
    cu accent_color; restul barelor rămân gri neutru — la fel cum Sky Sports evidențiază
    echipa/jucătorul discutat într-un clasament cu 15-20 de intrări."""
    fig, ax = plt.subplots(figsize=(width_cm / 2.54, height_cm / 2.54), dpi=150)
    bar_colors = [accent_hex if lbl == highlight_label else muted_grey for lbl in labels]
    bars = ax.barh(labels, values, color=bar_colors)
    ax.invert_yaxis()  # primul element din labels sus, ca într-un clasament citit de sus în jos
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", loc="left", pad=8)
    ax.tick_params(labelsize=8)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for b, v in zip(bars, values):
        ax.text(b.get_width(), b.get_y() + b.get_height() / 2, "  " + value_fmt.format(v),
                 va="center", fontsize=7.5)
    fig.tight_layout()
    path = _chart_path("bar", title, tuple(labels), tuple(values), highlight_label)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return RLImage(path, width=width_cm * cm, height=height_cm * cm)


def scatter_chart(labels, x_vals, y_vals, x_label="", y_label="", title="",
                   highlight_labels=None, width_cm=16.8, height_cm=8.5):
    """Grafic scatter simplu cu etichete — ex: puncte vs goluri marcate de la numirea unui
    antrenor, comparat cu restul ligii. `highlight_labels` (opțional, listă) marchează cu
    accent_color și bold punctele echipelor/jucătorilor discutați; restul rămân gri neutru."""
    highlight_set = set(highlight_labels or [])
    fig, ax = plt.subplots(figsize=(width_cm / 2.54, height_cm / 2.54), dpi=150)
    for lbl, x, y in zip(labels, x_vals, y_vals):
        is_hl = lbl in highlight_set
        ax.scatter(x, y, color=accent_hex if is_hl else muted_grey,
                    s=42 if is_hl else 24, zorder=3 if is_hl else 2)
        ax.annotate(lbl, (x, y), fontsize=7, xytext=(4, 2), textcoords="offset points",
                     fontweight="bold" if is_hl else "normal",
                     color=accent_hex if is_hl else "#555555")
    ax.set_xlabel(x_label, fontsize=8)
    ax.set_ylabel(y_label, fontsize=8)
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", loc="left", pad=8)
    ax.tick_params(labelsize=7.5)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    path = _chart_path("scatter", title, tuple(labels), tuple(x_vals), tuple(y_vals))
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return RLImage(path, width=width_cm * cm, height=height_cm * cm)


# ---------------------------------------------------------------------------
# 5. SCHELET DE DOCUMENT (exemplu de utilizare)
# ---------------------------------------------------------------------------
def build_example():
    doc = SimpleDocTemplate(
        "/home/claude/pachet_comentator_EXEMPLU.pdf", pagesize=A4,
        topMargin=1.3 * cm, bottomMargin=1.3 * cm, leftMargin=1.4 * cm, rightMargin=1.4 * cm,
        title="Exemplu pachet comentator",
    )
    story = []

    story.append(Paragraph("ECHIPA A v ECHIPA B", title))
    story.append(Paragraph("Competiție — dată — stadion, oră", subtitle))

    story.append(band_bar("STORY OF THE MATCH"))
    story.append(Spacer(1, 6))
    for f in ["Fapt interesant unu.", "Fapt interesant doi."]:
        story.append(Paragraph("•  " + f, bullet))

    # --- exemplu de bară de poveste dedicată, cu grafic bar simplu ---
    story.append(Paragraph("TITLU PUNCHY DE POVESTE", sect))
    story.append(Paragraph("•  Bullet-ul central al poveștii.", bullet))
    story.append(bar_chart(
        labels=["Echipa A", "Echipa X", "Echipa Y", "Echipa Z"],
        values=[42, 48, 52, 55],
        title="% dueluri câștigate — etapa curentă",
        highlight_label="Echipa A",
        value_fmt="{:.0f}%",
    ))
    story.append(Spacer(1, 8))

    story.append(band_bar("CAP LA CAP"))
    story.append(Spacer(1, 6))
    h2h = [
        [Paragraph("Dată", cellb), Paragraph("Meci", cellb), Paragraph("Scor", cellb)],
        [Paragraph("...", cell), Paragraph("...", cell), Paragraph("...", cell)],
    ]
    story.append(simple_table(h2h, [3.4, 9.8, 3.4]))

    story.append(band_bar("LOTURI COMPLETE"))
    story.append(Spacer(1, 6))
    squad_block(story, "Portari", [
        ("1", "Nume Jucător", 25, "ROU", "1,90m — titular, notă relevantă"),
    ], row_fn=squad_row_simple)

    story.append(Spacer(1, 10))
    story.append(Paragraph("Surse: ... Compilat pe [dată].", foot))

    doc.build(story)
    print("PDF exemplu generat.")


if __name__ == "__main__":
    build_example()
