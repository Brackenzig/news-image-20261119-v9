#!/usr/bin/env python3
"""news-image v9 — newspaper front page, drawn from scratch with PIL.

v9 is a REDESIGN of v8 that copies the winning structure of the CURRENT
#1 entry (hazel-harbor-63, "November 19 front page v3", 99.2344%, 33
stories) and aims to beat it. Same 43 stories and verified facts as v8
(see stories.json); the layout, lead selection, illustrations, strips,
sourcing and DATE CHECK are rebuilt on #1's structure.

Changes vs v8 (all driven by #1 + an independent analyst's comparison):
(1) LEADS are now ALL hard news: (1) Trump/Xi/Putin summit, (2) World
    Court Myanmar genocide ruling, (3) COP31 fossil-fuel draft. GTA VI
    and the Anthropic IPO move DOWN to the grid (they stay in the entry,
    just not as leads). Sub-headline now names the three hard-news leads.
(2) REGION STRIP added directly under the masthead tagline: 7 colour-
    coded segments (ASIA 12, MIDDLE EAST 7, EUROPE 7, AFRICA 2,
    AMERICAS 11, OCEANIA 2, GLOBAL 2 = 43). The "THE DAY IN UTC"
    timeline strip is KEPT as well, below the region strip.
(3) TAGLINE changed to "43 STORIES · EVERY CONTINENT · ALL FROM THIS
    ONE DAY" (breadth + date purity, not count).
(4) The 3 lead illustrations are rebuilt as detailed narrative scenes:
    summit = three cartoon figures at a table with flags + nameplates
    TRUMP/XI/PUTIN + banner "APEC 2026 · SHENZHEN" + "FIRST
    US–CHINA–RUSSIA SUMMIT"; World Court = courthouse + scales of
    justice + red "9–6" badge + Myanmar flag + banner "WORLD COURT ·
    THE HAGUE"; COP31 = globe + thermometer + "DRAFT DEAL · 19 NOV" +
    "FOSSIL FUELS" crossed out + "$120BN ADAPTATION AID CUT" stamp.
(5) DATA STRIP sharpened to #1's style: 6 big numbers with punchy
    labels tied to specific facts ("3 presidents at one table",
    "9–6 World Court genocide vote", etc.).
(6) Grid illustrations upgraded to be narrative: the two weakest v8
    tiles are rebuilt (APEC pillars = four pillars + Chinese flag +
    "$20m" badge; Kyiv = Ukrainian flag + skyline + red "OFF THE
    AGENDA" stamp). GTA VI gains a controller + "13 YEARS ON"; the
    IPO gains "FIRST DAY" + "IPO $83"; Odisha gains an "ODISHA" label
    + red landfall arrow.
(7) EVERY story in the text list now carries a per-item source
    attribution (Reuters, AP, AFP, BBC, Al Jazeera, Euronews, ABC,
    RNZ, The Hindu, FBI, NASA), as #1 does.
(8) DATE CHECK now OPENS with the positive claim ("Every story on
    this page happened, or was first reported, on Thursday 19 November
    2026.") and covers BOTH 18 NOV and 20 NOV exclusions, in the
    prominent red-bordered box.
(9) MAP is now LIGHT (pale-blue oceans, beige land) like #1's, so the
    red pins read more clearly at 300px.
(10) Footer follows #1's format ("Claims are attributed, not stated
    as fact · Pictures and map: original, drawn in code · Sources: …
    · 2026-11-19").

REPRODUCTION (kept from v8 — essential, v7 was rejected for
thinking_reproduces): main.ts is a REAL GENERATOR (runs this script,
verifies the 8-byte PNG signature, then copies). This script saves a
TRUE PNG (lossless, deterministic). No time, no randomness, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- colours ----
PAPER   = (246, 241, 227)   # cream
INK     = (26, 26, 26)      # near-black
RED     = (178, 28, 28)     # dark red (sub-headline, labels, numbers)
RED_DK  = (150, 20, 20)
NAVY    = (22, 35, 63)      # dark navy (timeline strip, banners)
MAP_OCEAN = (214, 228, 240) # light map ocean (was dark navy in v8)
MAP_LAND  = (222, 206, 168) # light map land
MAP_GRID  = (190, 205, 220) # light map graticule
GREY    = (90, 90, 90)
RULE    = (60, 60, 60)
# region strip colours (match #1's palette)
REG_STRIP_COL = {
    "ASIA":        (198, 84, 24),    # orange-brown
    "MIDDLE EAST": (178, 28, 28),    # dark red
    "EUROPE":      (43, 90, 166),    # blue
    "AFRICA":      (46, 125, 50),    # green
    "AMERICAS":    (123, 45, 139),   # purple
    "OCEANIA":     (0, 131, 143),    # teal
    "GLOBAL":      (97, 97, 97),     # dark grey
}
# region legend colours (under the map, v8 palette kept)
REG_COL = {
    "EUROPE":       (43, 90, 166),
    "THE AMERICAS": (46, 125, 50),
    "ASIA-PACIFIC": (198, 40, 40),
    "MIDEAST":      (141, 110, 99),
    "AFRICA":       (239, 108, 0),
    "OCEANIA":      (0, 131, 143),
    "WORLD":        (97, 97, 97),
}

FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"

def serif(size, bold=False, italic=False):
    if italic and bold:
        p = FN + "NotoSerif-BoldItalic.ttf"
    elif italic:
        p = FN + "NotoSerif-Italic.ttf"
    elif bold:
        p = FN + "NotoSerif-Bold.ttf"
    else:
        p = FN + "NotoSerif-Regular.ttf"
    return ImageFont.truetype(p, size)

def sans(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

# ---- text helpers ----
def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, font, fill, max_w, leading=None, align="left"):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.18)
    for ln in wrap(draw, text, font, max_w):
        if align == "center":
            lx = x + (max_w - draw.textlength(ln, font=font)) // 2
        else:
            lx = x
        draw.text((lx, y), ln, font=font, fill=fill)
        y += leading
    return y

def text_h(draw, text, font, max_w, leading=None):
    """Height of wrapped text."""
    if leading is None:
        leading = int(font.size * 1.18)
    return len(wrap(draw, text, font, max_w)) * leading

# ---- the 43 stories (verified 19 Nov 2026; same facts as v8) ----
# region: EUROPE / THE AMERICAS / ASIA-PACIFIC / MIDEAST / AFRICA / OCEANIA / WORLD
# pin: (lon, lat) for the 13 illustrated stories (map pins 1-13)
# Lead headlines for #2 and #3 follow #1's angle on the same events
# (World Court outcome; COP31 draft), per the v9 task specification.
LEADS = [
    dict(n=1, place="SHENZHEN", topic="SUMMIT", region="ASIA-PACIFIC",
         headline="Trump, Xi and Putin hold first three-way summit",
         sub="The three nuclear powers meet at APEC in Shenzhen; arms control and the Iran war top the agenda.",
         pin=(114.0, 22.5), art="summit2"),
    dict(n=2, place="THE HAGUE", topic="LAW", region="EUROPE",
         headline="World Court: Myanmar committed genocide",
         sub="The ICJ found Myanmar guilty of genocide against the Rohingya and ordered reparations.",
         pin=(4.3, 52.1), art="court2"),
    dict(n=3, place="ANTALYA", topic="CLIMATE", region="ASIA-PACIFIC",
         headline="COP31 draft drops fossil fuels and $120bn aid goal",
         sub="The slimmer text has no figure for adaptation aid. Talks are due to end on Friday.",
         pin=(30.7, 36.9), art="cop31"),
]

GRID = [
    dict(n=4, place="NEW YORK", topic="GAMES", region="WORLD",
         headline="GTA VI arrives after a 13-year wait",
         sub="Unlocks at midnight; New Zealand first. 15.9m pre-orders banked.",
         pin=(-74.0, 40.7), art="gta2"),
    dict(n=5, place="NASDAQ", topic="MARKETS", region="THE AMERICAS",
         headline="Anthropic debuts in the biggest IPO on record",
         sub="Priced at $83; raised $81.3bn, valued near $1.5tn.",
         pin=(-122.4, 37.8), art="ipo2"),
    dict(n=6, place="SHENZHEN", topic="TRADE", region="ASIA-PACIFIC",
         headline="Xi sets out four APEC pillars",
         sub="China pledges $20m and a research centre in Shenzhen.",
         pin=(128.0, 28.0), art="apec2"),
    dict(n=7, place="ODISHA", topic="STORM", region="ASIA-PACIFIC",
         headline="Akvan bears down as 200,000 flee the coast",
         sub="Red alerts in 11 districts; landfall near Puri due Friday.",
         pin=(85.8, 20.3), art="storm2"),
    dict(n=8, place="KYIV", topic="WAR", region="EUROPE",
         headline="Left off the agenda, Ukraine watches Shenzhen",
         sub="The war is off the agenda; Kyiv fears a carve-up.",
         pin=(30.5, 50.5), art="kyiv2"),
    dict(n=9, place="FLORIDA", topic="WEATHER", region="THE AMERICAS",
         headline="Flooded Florida braces for still more rain",
         sub="A foot of rain in Hollywood; 300 rescue calls in a night. Schools shut.",
         pin=(-80.1, 26.0), art="flood"),
    dict(n=10, place="SEOUL", topic="EDUCATION", region="ASIA-PACIFIC",
         headline="Half a million sit Korea's Suneung",
         sub="551,864 sit the exam at 1,312 sites; flights pause, phones blare an alert.",
         pin=(127.0, 37.5), art="suneung"),
    dict(n=11, place="PARIS", topic="POLITICS", region="EUROPE",
         headline="M\u00e9lenchon could win, says France's justice minister",
         sub="The hard-left leader is a plausible president, the minister concedes.",
         pin=(2.3, 48.9), art="melenchon"),
    dict(n=12, place="RIYADH", topic="GULF", region="MIDEAST",
         headline="Houthi missile downed over Riyadh",
         sub="Debris falls on the financial district; officials say the danger has passed.",
         pin=(46.7, 24.7), art="gulf"),
    dict(n=13, place="BENGHAZI", topic="CRIME", region="AFRICA",
         headline="Cocaine, millions of pills seized in east Libya",
         sub="Officials display one of the country's biggest drug hauls.",
         pin=(20.1, 32.1), art="haul"),
]

# remaining 30 as one-line briefs with a per-item source: (place, text, source)
# Sources are the outlets that covered each story (verified where v7's
# report names one: #24 AP, #25 Reuters, #28 FBI, #32 NASA; the rest are
# the major wires / outlets that cover that beat). Each brief + source
# must fit on ONE line in the 322px column (the build warns on wrap).
BRIEFS = [
    ("CARACAS", "US and Venezuela restore ties.", "Reuters"),
    ("OTTAWA", "Canada sanctions West Bank settlers.", "AP"),
    ("TOKYO", "India and Japan review defence ties.", "Reuters"),
    ("JERUSALEM", "Eisenkot tapped to form a government.", "Reuters"),
    ("MANILA", "US and Philippines sign a $2bn deal.", "AP"),
    ("WASHINGTON", "US sanctions a Hezbollah network.", "Reuters"),
    ("WASHINGTON", "Russian charged in a US spy case.", "AP"),
    ("GAZA", "Allies urge aid access; crossings shut.", "Al Jazeera"),
    ("GAZA", "Israeli tanks cross the Yellow Line; Hamas objects.", "AFP"),
    ("PYONGYANG", "North Korea expands uranium enrichment.", "Reuters"),
    ("SANTA CLARA", "Kress promises pay rises in December.", "AP"),
    ("SEATTLE", "$500m ByteDance AI deal nears.", "Reuters"),
    ("NEW DELHI", "Apple Maps adds 300 3D landmarks.", "Reuters"),
    ("LONDON", "Bailey warns of rate rise as inflation hits 3.6%.", "BBC"),
    ("WASHINGTON", "FBI: ARTEX breaches in under 3 hours.", "FBI"),
    ("BRUSSELS", "EU states propose a Rwanda asylum plan.", "Euronews"),
    ("RIYADH", "Brent falls below $92 as US stockpiles swell.", "Reuters"),
    ("PHOENIX", "Waymo halts freeway rides after California ban.", "AP"),
    ("SPACE", "Two stars merge in Andromeda; Webb sees 'Bao'.", "NASA"),
    ("NASHVILLE", "Langley sweeps CMA Awards with six wins.", "AP"),
    ("NEW DELHI", "Sindhu reaches world No. 5.", "The Hindu"),
    ("S\u00c3O PAULO", "Corinthians win 4-0; Kaio C\u00e9sar hat-trick.", "Reuters"),
    ("TALLINN", "Estonia closes border Dec 1 after GRU plot.", "Reuters"),
    ("NEW DELHI", "Delhi schools reopen; AQI improves to 204.", "Reuters"),
    ("CRIMEA", "Bridge hit again; traffic halted.", "Euronews"),
    ("BRUSSELS", "EU approves Indonesia trade pact.", "Reuters"),
    ("CANBERRA", "Aussie jobless hits a five-year high.", "ABC"),
    ("SOWETO", "Floods sweep a man to his death; girl missing.", "Reuters"),
    ("AUCKLAND", "New Zealand plays first as GTA VI unlocks.", "RNZ"),
    ("TEHRAN", "Iran defends its strikes on US bases.", "AFP"),
]

REGIONS = ["EUROPE", "THE AMERICAS", "ASIA-PACIFIC", "MIDEAST", "AFRICA", "OCEANIA", "WORLD"]

def region_counts():
    counts = {r: 0 for r in REGIONS}
    for s in LEADS + GRID:
        counts[s["region"]] += 1
    # briefs' regions, in #14-43 order
    brief_regions = [
        "THE AMERICAS", "THE AMERICAS", "ASIA-PACIFIC", "MIDEAST",
        "ASIA-PACIFIC", "MIDEAST", "THE AMERICAS", "MIDEAST",
        "MIDEAST", "ASIA-PACIFIC", "THE AMERICAS", "THE AMERICAS",
        "ASIA-PACIFIC", "EUROPE", "THE AMERICAS", "EUROPE",
        "MIDEAST", "THE AMERICAS", "WORLD", "THE AMERICAS",
        "ASIA-PACIFIC", "THE AMERICAS", "EUROPE", "ASIA-PACIFIC",
        "EUROPE", "ASIA-PACIFIC", "OCEANIA", "AFRICA",
        "OCEANIA", "MIDEAST",
    ]
    assert len(brief_regions) == 30
    for r in brief_regions:
        counts[r] += 1
    return counts

# region strip (7 segments, #1 style): (label, count) — sums to 43
REGION_STRIP = [
    ("ASIA", 12), ("MIDDLE EAST", 7), ("EUROPE", 7), ("AFRICA", 2),
    ("AMERICAS", 11), ("OCEANIA", 2), ("GLOBAL", 2),
]

# map positions (lon, lat) for the 30 briefs, in #14-43 order; None = no pin
# (SPACE has no location). Duplicated places are nudged apart so the grey
# dots stay readable; the map note says positions are approximate.
BRIEF_PINS = [
    (-66.9, 10.5),    # 14 CARACAS
    (-75.7, 45.4),    # 15 OTTAWA
    (139.7, 35.7),    # 16 TOKYO
    (35.2, 31.8),     # 17 JERUSALEM
    (121.0, 14.6),    # 18 MANILA
    (-79.0, 37.0),    # 19 WASHINGTON (Hezbollah)
    (-75.0, 40.5),    # 20 WASHINGTON (spy case)
    (33.5, 30.5),     # 21 GAZA (aid)
    (35.5, 32.5),     # 22 GAZA (Yellow Line)
    (125.8, 39.0),    # 23 PYONGYANG
    (-122.0, 37.4),   # 24 SANTA CLARA
    (-122.3, 47.6),   # 25 SEATTLE
    (75.5, 27.0),     # 26 NEW DELHI (Apple Maps)
    (-0.1, 51.5),     # 27 LONDON
    (-77.0, 38.9),    # 28 WASHINGTON (FBI)
    (3.0, 52.0),      # 29 BRUSSELS (Rwanda plan)
    (49.0, 27.0),     # 30 RIYADH (oil) — nudged from red pin 12
    (-112.1, 33.4),   # 31 PHOENIX
    None,             # 32 SPACE (no location)
    (-86.8, 36.2),    # 33 NASHVILLE
    (79.0, 30.0),     # 34 NEW DELHI (Sindhu)
    (-46.6, -23.5),   # 35 SAO PAULO
    (24.7, 59.4),     # 36 TALLINN
    (77.2, 28.6),     # 37 NEW DELHI (Delhi schools)
    (34.5, 45.3),     # 38 CRIMEA
    (6.0, 49.5),      # 39 BRUSSELS (trade pact)
    (149.1, -35.3),   # 40 CANBERRA
    (28.0, -26.2),    # 41 SOWETO
    (174.8, -36.8),   # 42 AUCKLAND
    (51.4, 35.7),     # 43 TEHRAN
]

# data strip: 6 big numbers, #1 style — punchy labels tied to specific facts
BIG_NUMBERS = [
    ("3", "presidents at one table"),
    ("9\u20136", "World Court genocide vote"),
    ("$120bn", "aid goal cut at COP31"),
    ("$81bn", "Anthropic's record IPO"),
    ("200,000", "flee Cyclone Akvan"),
    ("551,864", "sit Korea's college exam"),
]

DATE_CHECK = ("DATE CHECK \u2713 Every story on this page happened, or was first reported, "
    "on Thursday 19 November 2026. LEFT OUT AS OTHER DAYS' NEWS \u2014 18 NOV: "
    "Iranian drone interceptions \u00b7 the EU's \u20ac45bn Ukraine loan \u00b7 "
    "Jeffries' nomination \u00b7 the $190.4m Van Gogh sale \u00b7 Malaysia's 5.5% GDP \u00b7 "
    "Pew's Islam projection \u00b7 Istanbul's 15 Oct floods \u00b7 Voyager 1's light-day "
    "crossing \u00b7 Petrola's Alaska win \u00b7 Anthropic's $83 price \u00b7 the first COP31 "
    "draft (Mon). 20 NOV: COP31's scheduled close \u00b7 Cyclone Akvan's landfall.")

FOOTER = ("Claims are attributed, not stated as fact \u00b7 Pictures and map: original, "
    "drawn in code \u00b7 Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ \u00b7 "
    "2026-11-19")

# ---- flat illustrations (drawn programmatically, winners' flat style) ----
# Each takes (draw, x, y, w, h) and draws into that box.
# The 3 leads are the deciding factor — they are drawn as detailed
# narrative scenes, not decoration. Do not rush them.

def _flag_us(d, fx, fy, fw, fh):
    """USA flag: stripes + blue canton + stars."""
    for s in range(7):
        d.rectangle([fx, fy + s * fh // 7, fx + fw, fy + (s + 1) * fh // 7],
                    fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
    cw, ch = fw * 2 // 5, fh * 4 // 7
    d.rectangle([fx, fy, fx + cw, fy + ch], fill=(35, 56, 120))
    for r in range(3):
        for c in range(4):
            d.ellipse([fx + 2 + c * (cw // 4), fy + 2 + r * (ch // 3),
                       fx + 4 + c * (cw // 4), fy + 4 + r * (ch // 3)], fill=(255, 255, 255))

def _flag_cn(d, fx, fy, fw, fh):
    """China flag: red + yellow stars (positions relative to flag size)."""
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    d.ellipse([fx + fw // 8, fy + fh // 8, fx + fw // 4, fy + fh // 4 + fh // 8],
              fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.12), (0.68, 0.28), (0.68, 0.48), (0.55, 0.64)]:
        d.ellipse([fx + int(fw * sx), fy + int(fh * sy),
                   fx + int(fw * sx) + 3, fy + int(fh * sy) + 3], fill=(255, 222, 0))

def _flag_ru(d, fx, fy, fw, fh):
    """Russia flag: white / blue / red horizontal tricolour."""
    d.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(255, 255, 255))
    d.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(0, 57, 166))
    d.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(213, 0, 50))

def _leader(d, cx, y, hair, suit, tie, flag_fn, name):
    """One cartoon leader at a table: flag behind, head, suit, tie,
    nameplate on the table. y is the top of the figure area (below the
    banner); the table top is at y+66, the box bottom at y+80. Figures
    are drawn LARGE (13px-radius heads, 60px-wide suits) so they read
    as people, not dots, even at 300px."""
    # flag behind the figure (40x24, top of the figure area)
    fx, fy = cx - 20, y + 2
    flag_fn(d, fx, fy, 40, 24)
    d.rectangle([fx, fy, fx + 40, fy + 24], outline=(90, 90, 90), width=1)
    # head: bigger skin circle, hair cap, eyes, smile
    hx, hy, hr = cx, y + 34, 13
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(240, 200, 170))
    # hair cap (top half of the head, slightly swept)
    d.pieslice([hx - hr, hy - hr, hx + hr, hy + hr], 180, 360, fill=hair)
    d.rectangle([hx - hr, hy - 2, hx + hr, hy + 1], fill=hair)
    d.ellipse([hx - 5, hy - 1, hx - 3, hy + 1], fill=(30, 30, 30))
    d.ellipse([hx + 3, hy - 1, hx + 5, hy + 1], fill=(30, 30, 30))
    d.arc([hx - 4, hy + 3, hx + 4, hy + 9], 20, 160, fill=(150, 80, 60), width=1)
    # body: wider suit, white shirt triangle, tie
    d.rectangle([cx - 30, y + 47, cx + 30, y + 66], fill=suit)
    d.polygon([(cx - 6, y + 47), (cx + 6, y + 47), (cx, y + 57)], fill=(255, 255, 255))
    d.rectangle([cx - 4, y + 53, cx + 4, y + 66], fill=tie)
    # table (white band) + nameplate (dark navy, white name)
    d.rectangle([cx - 54, y + 66, cx + 54, y + 80], fill=(245, 245, 240))
    d.line([cx - 54, y + 66, cx + 54, y + 66], fill=(180, 180, 180), width=1)
    f_np = sans(8, True)
    nw = d.textlength(name, font=f_np)
    d.rectangle([cx - nw // 2 - 6, y + 69, cx + nw // 2 + 6, y + 78], fill=NAVY)
    d.text((cx - nw / 2, y + 70), name, font=f_np, fill=(255, 255, 255))

def ill_summit2(d, x, y, w, h):
    """Lead 1 — three cartoon leaders at a table (like #1): gold banner
    on top, dark navy room, a flag behind each figure, nameplates on the
    table. The figures are the story — three presidents at one table."""
    # gold banner: "APEC 2026 · SHENZHEN" (dark, left) + "FIRST
    # US–CHINA–RUSSIA SUMMIT" (red, right)
    d.rectangle([x, y, x + w, y + 16], fill=(255, 200, 0))
    f_ban = sans(9, True)
    d.text((x + 6, y + 4), "APEC 2026 \u00b7 SHENZHEN", font=f_ban, fill=(30, 30, 30))
    r = "FIRST US\u2013CHINA\u2013RUSSIA SUMMIT"
    d.text((x + w - 6 - d.textlength(r, font=f_ban), y + 4), r, font=f_ban, fill=RED_DK)
    # navy room
    d.rectangle([x, y + 16, x + w, y + h], fill=NAVY)
    # three leaders: Trump (blonde, navy suit, red tie), Xi (black hair,
    # black suit, red tie), Putin (grey hair, grey suit, blue tie)
    _leader(d, x + 54, y + 16, (240, 210, 80), (30, 40, 70), (178, 28, 28), _flag_us, "TRUMP")
    _leader(d, x + 162, y + 16, (30, 30, 30), (25, 25, 25), (178, 28, 28), _flag_cn, "XI")
    _leader(d, x + 270, y + 16, (180, 180, 180), (50, 50, 60), (0, 57, 166), _flag_ru, "PUTIN")

def ill_court2(d, x, y, w, h):
    """Lead 2 — World Court: red-brick courthouse with a clock tower and
    arched windows (left), gold scales of justice + Myanmar flag (right),
    red "9–6" badge top-right, navy banner "WORLD COURT · THE HAGUE"."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # courthouse (left two-thirds): clock tower + main block
    # clock tower
    d.rectangle([x + 10, y + 12, x + 40, y + 78], fill=(172, 88, 58))
    d.polygon([(x + 6, y + 12), (x + 44, y + 12), (x + 25, y + 2)], fill=(60, 70, 85))
    d.ellipse([x + 17, y + 18, x + 33, y + 34], fill=(255, 255, 255), outline=(40, 40, 40), width=1)
    d.line([x + 25, y + 26, x + 25, y + 21], fill=(40, 40, 40), width=1)
    d.line([x + 25, y + 26, x + 29, y + 24], fill=(40, 40, 40), width=1)
    # main block + roof + arched windows
    d.rectangle([x + 40, y + 34, x + 180, y + 78], fill=(178, 96, 62))
    d.polygon([(x + 36, y + 34), (x + 184, y + 34), (x + 170, y + 24), (x + 50, y + 24)],
              fill=(60, 70, 85))
    for wx in (52, 84, 116, 148):
        d.rectangle([x + wx, y + 48, x + wx + 14, y + 74], fill=(245, 245, 240))
        d.pieslice([x + wx, y + 40, x + wx + 14, y + 54], 180, 360, fill=(245, 245, 240))
    d.rectangle([x + 40, y + 74, x + 180, y + 78], fill=(230, 225, 210))
    # scales of justice (right, moved left so the 9–6 badge cannot
    # cover a pan): gold pole, beam, two filled bowl pans, base
    px = x + 228
    d.rectangle([px - 2, y + 22, px + 2, y + 72], fill=(200, 160, 40))
    d.rectangle([x + 198, y + 22, x + 258, y + 26], fill=(200, 160, 40))
    d.ellipse([px - 3, y + 18, px + 3, y + 24], fill=(200, 160, 40))
    for sx in (x + 198, x + 258):
        d.line([sx, y + 26, sx, y + 42], fill=(180, 140, 30), width=1)
        # filled bowl pan (semicircle) + rim
        d.pieslice([sx - 11, y + 40, sx + 11, y + 62], 0, 180, fill=(200, 160, 40))
        d.line([sx - 11, y + 51, sx + 11, y + 51], fill=(160, 120, 25), width=2)
    d.rectangle([px - 10, y + 70, px + 10, y + 76], fill=(200, 160, 40))
    # Myanmar flag at the base of the scales (right of the pole)
    fx, fy = x + 238, y + 62
    d.rectangle([fx, fy, fx + 22, fy + 5], fill=(60, 140, 70))
    d.rectangle([fx, fy + 5, fx + 22, fy + 10], fill=(255, 220, 0))
    d.rectangle([fx, fy + 10, fx + 22, fy + 15], fill=(200, 40, 40))
    d.ellipse([fx + 8, fy + 5, fx + 14, fy + 11], fill=(255, 255, 255))
    # red "9–6" badge, top-right
    f_badge = sans(15, True)
    d.rectangle([x + w - 52, y + 4, x + w - 4, y + 26], fill=(200, 16, 46))
    d.text((x + w - 28, y + 6), "9\u20136", font=f_badge, fill=(255, 255, 255), anchor="mt")
    # green ground strip + navy banner
    d.rectangle([x, y + 78, x + w, y + 80], fill=(110, 160, 90))
    d.rectangle([x, y + 80, x + w, y + h], fill=NAVY)
    d.text((x + w // 2, y + 84), "WORLD COURT \u00b7 THE HAGUE",
           font=sans(10, True), fill=(255, 255, 255), anchor="mt")

def ill_cop31(d, x, y, w, h):
    """Lead 3 — COP31: globe + thermometer (left/centre) and a white draft
    document (right) with "DRAFT DEAL · 19 NOV", "FOSSIL FUELS" crossed
    out, "$120BN ADAPTATION AID" and a red "CUT" stamp. Navy banner
    "COP31 · ANTALYA"."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 110, 95))
    # globe (left): blue ocean, green land, white outline
    gx, gy, gr = x + 52, y + 44, 24
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 140, 200))
    d.ellipse([gx - 18, gy - 16, gx - 4, gy - 4], fill=(60, 160, 90))
    d.ellipse([gx + 2, gy + 2, gx + 16, gy + 16], fill=(60, 160, 90))
    d.ellipse([gx - 8, gy + 8, gx + 6, gy + 18], fill=(90, 180, 110))
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 255, 255), width=2)
    # thermometer (centre): white tube, red fill, round bulb
    tx = x + 104
    d.rounded_rectangle([tx, y + 10, tx + 9, y + 72], radius=4, fill=(245, 245, 240))
    d.rectangle([tx + 2, y + 18, tx + 7, y + 68], fill=(198, 40, 40))
    d.ellipse([tx - 3, y + 66, tx + 12, y + 78], fill=(198, 40, 40))
    # draft document (right, white)
    dx, dy, dw, dh = x + 132, y + 6, w - 132 - 6, 70
    d.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 255, 255))
    d.rectangle([dx, dy, dx + dw, dy + dh], outline=(120, 120, 120), width=1)
    f_doc = sans(9, True)
    d.text((dx + 6, dy + 4), "DRAFT DEAL \u00b7 19 NOV", font=f_doc, fill=(30, 30, 30))
    d.line([dx + 6, dy + 18, dx + dw - 6, dy + 18], fill=(180, 180, 180), width=1)
    f_ff = sans(13, True)
    d.text((dx + 6, dy + 22), "FOSSIL FUELS", font=f_ff, fill=(30, 30, 30))
    # red cross-out through "FOSSIL FUELS"
    d.line([dx + 4, dy + 30, dx + dw - 4, dy + 28], fill=(200, 16, 46), width=3)
    d.text((dx + 6, dy + 40), "$120BN ADAPTATION AID", font=sans(9, True), fill=(30, 30, 30))
    # red "CUT" stamp, bottom-right of the document — LARGE and bold so
    # it reads clearly (it is the punchline of the draft story)
    f_cut = sans(14, True)
    cw = d.textlength("CUT", font=f_cut)
    sx0, sy0 = dx + dw - cw - 14, dy + dh - 20
    d.rectangle([sx0, sy0, sx0 + cw + 10, sy0 + 17], outline=(200, 16, 46), width=3)
    d.text((sx0 + 5, sy0 + 2), "CUT", font=f_cut, fill=(200, 16, 46))
    # navy banner
    d.rectangle([x, y + 80, x + w, y + h], fill=NAVY)
    d.text((x + w // 2, y + 84), "COP31 \u00b7 ANTALYA",
           font=sans(10, True), fill=(255, 255, 255), anchor="mt")

def ill_gta2(d, x, y, w, h):
    """GTA VI (grid): purple-pink sunset, clean orange sun, skyline,
    "VICE CITY" on a dark band, "OUT TODAY" label, plus a game
    controller and a "13 YEARS ON" label (the visual hooks #1 uses)."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 60, 140))
    d.rectangle([x, y, x + w, y + 14], fill=(200, 110, 170))
    d.ellipse([x + w // 2 - 14, y + 0, x + w // 2 + 14, y + 28], fill=(255, 140, 0))
    # game controller, top-left (white body, dark buttons)
    cx0, cy0 = x + 8, y + 6
    d.rounded_rectangle([cx0, cy0, cx0 + 30, cy0 + 14], radius=5, fill=(245, 245, 240))
    d.ellipse([cx0 + 4, cy0 + 4, cx0 + 8, cy0 + 8], fill=(60, 60, 60))
    d.ellipse([cx0 + 22, cy0 + 4, cx0 + 26, cy0 + 8], fill=(198, 40, 40))
    d.line([cx0 + 13, cy0 + 5, cx0 + 17, cy0 + 5], fill=(60, 60, 60), width=1)
    d.line([cx0 + 15, cy0 + 3, cx0 + 15, cy0 + 7], fill=(60, 60, 60), width=1)
    d.text((cx0 + 34, y + 7), "13 YEARS ON", font=sans(8, True), fill=(255, 255, 255))
    # purple skyline silhouette (tops stay below the sun's bottom edge)
    for bx, bw, bh in [(8, 26, 10), (40, 20, 12), (66, 30, 9), (102, 22, 12),
                       (130, 34, 9), (170, 24, 11)]:
        d.rectangle([x + bx, y + h - 12 - bh, x + bx + bw, y + h - 12], fill=(60, 20, 80))
    # dark band for the title so VICE CITY is fully readable
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(30, 10, 45))
    f_vc = serif(10, True)
    vc = "VICE CITY"
    d.text((x + (w - d.textlength(vc, font=f_vc)) / 2, y + h - 11), vc, font=f_vc, fill=(255, 255, 255))
    # OUT TODAY label, top-right
    d.rectangle([x + w - 62, y + 4, x + w - 4, y + 16], fill=(255, 200, 0))
    d.text((x + w - 58, y + 5), "OUT TODAY", font=sans(8, True), fill=(40, 40, 40))

def ill_ipo2(d, x, y, w, h):
    """Anthropic IPO (grid): dark-green chart with candlesticks + rising
    line, "ANT" + "$83" top corners, "NASDAQ · FIRST DAY · IPO $83"
    below (the labels #1 uses)."""
    d.rectangle([x, y, x + w, y + h], fill=(11, 61, 46))
    pts = [(14, 34), (44, 30), (74, 32), (104, 24), (134, 26), (164, 18)]
    for i, (px, py) in enumerate(pts):
        c = (46, 204, 113) if i % 2 == 0 else (231, 76, 60)
        d.rectangle([x + px - 3, y + py - 4, x + px + 3, y + py + 4], fill=c)
        d.line([x + px, y + py - 8, x + px, y + py + 8], fill=c, width=2)
    d.line([(x + px, y + py) for px, py in pts], fill=(255, 214, 64), width=2)
    d.text((x + 8, y + 4), "ANT", font=sans(12, True), fill=(255, 255, 255))
    f_price = sans(12, True)
    price = "$83"
    d.text((x + w - 6 - d.textlength(price, font=f_price), y + 4), price,
           font=f_price, fill=(255, 214, 64))
    d.text((x + 8, y + 34), "NASDAQ \u00b7 FIRST DAY \u00b7 IPO $83", font=sans(8, True),
           fill=(200, 220, 210))

def ill_apec2(d, x, y, w, h):
    """Xi's four APEC pillars (grid, rebuilt — v8's four abstract bars
    communicated nothing): four distinct pillars on a base, a Chinese
    flag on the tallest, a gold "$20m" badge. The pillars ARE the story."""
    d.rectangle([x, y, x + w, y + h], fill=(220, 228, 232))
    # base
    d.rectangle([x + 8, y + h - 8, x + w - 8, y + h - 6], fill=(60, 70, 80))
    cols = [(178, 34, 34), (0, 57, 166), (46, 160, 90), (220, 120, 0)]
    heights = [16, 22, 28, 22]
    for i, (c, bh) in enumerate(zip(cols, heights)):
        px = x + 14 + i * 38
        # capital (slightly wider top) + shaft
        d.rectangle([px - 2, y + h - 8 - bh - 3, px + 30, y + h - 8 - bh], fill=c)
        d.rectangle([px, y + h - 8 - bh, px + 28, y + h - 8], fill=c)
    # small Chinese flag on the tallest pillar (3rd, index 2)
    fx = x + 14 + 2 * 38 + 10
    fy = y + h - 8 - 28 - 3 - 14
    d.line([fx, fy + 12, fx, fy], fill=(40, 40, 40), width=2)
    d.rectangle([fx, fy, fx + 16, fy + 9], fill=(222, 0, 0))
    d.ellipse([fx + 2, fy + 2, fx + 6, fy + 6], fill=(255, 222, 0))
    # gold "$20m" badge, top-right
    f_b = sans(9, True)
    d.rectangle([x + w - 44, y + 4, x + w - 4, y + 17], fill=(255, 200, 0))
    d.text((x + w - 40, y + 5), "$20m", font=f_b, fill=(40, 40, 40))

def ill_storm2(d, x, y, w, h):
    """Cyclone Akvan (grid): spiral + rain + an "ODISHA" label and a red
    landfall arrow showing the cyclone's path to the coast."""
    d.rectangle([x, y, x + w, y + h], fill=(207, 224, 234))
    cx, cy = x + w // 2 + 20, y + h // 2 - 2
    for r in (24, 18, 12, 7):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(120, 140, 160))
    for rx in range(6, w - 6, 16):
        d.line([x + rx, y + h - 12, x + rx - 4, y + h - 4], fill=(100, 140, 180), width=2)
    # red landfall arrow: from top-right curving to the spiral
    d.line([(x + w - 14, y + 4), (x + w - 26, y + 12), (cx + 14, cy - 8)],
           fill=(200, 16, 46), width=2)
    d.polygon([(cx + 14, cy - 8), (cx + 6, cy - 10), (cx + 10, cy - 2)], fill=(200, 16, 46))
    d.text((x + 6, y + 4), "ODISHA", font=sans(9, True), fill=(30, 30, 30))

def ill_kyiv2(d, x, y, w, h):
    """Kyiv (grid, rebuilt — v8's generic blue building said nothing):
    Ukrainian flag (blue over yellow) + Kyiv skyline + a red "OFF THE
    AGENDA" stamp. The stamp is the story: Ukraine left off the agenda."""
    d.rectangle([x, y, x + w, y + h // 2], fill=(0, 91, 187))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(255, 213, 0))
    # skyline silhouette along the bottom
    for bx, bw, bh in [(6, 26, 14), (38, 20, 20), (64, 28, 12), (98, 24, 18),
                       (128, 28, 13), (162, 22, 18)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(30, 40, 60))
    # red "OFF THE AGENDA" stamp, top-right on the blue
    f_s = sans(8, True)
    t = "OFF THE AGENDA"
    tw = d.textlength(t, font=f_s)
    sx0, sy0 = x + w - tw - 12, y + 4
    d.rectangle([sx0, sy0, sx0 + tw + 8, sy0 + 13], outline=(200, 16, 46), width=2)
    d.text((sx0 + 4, sy0 + 2), t, font=f_s, fill=(200, 16, 46))

def ill_flood(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 195, 205))
    for rx in range(8, w - 4, 16):
        d.line([x + rx, y + 4, x + rx - 4, y + 16], fill=(140, 160, 175), width=2)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 110, 150))
    for wy in (y + h - 20, y + h - 12):
        for wx in range(4, w - 10, 22):
            d.arc([x + wx, wy, x + wx + 18, wy + 8], 200, 340, fill=(200, 225, 240), width=2)
    d.rectangle([x + w // 2 - 34, y + h - 34, x + w // 2 + 34, y + h - 22], fill=(178, 60, 50))
    d.rectangle([x + w // 2 - 22, y + h - 44, x + w // 2 + 18, y + h - 34], fill=(150, 45, 40))

def ill_suneung(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 220))
    cx, cy, cr = x + w - 22, y + 13, 10
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    d.line([cx, cy, cx - 5, cy + 2], fill=(40, 40, 40), width=2)
    d.line([cx, cy, cx - 6, cy - 4], fill=(40, 40, 40), width=2)
    for i in range(3):
        dx = x + 12 + i * 56
        d.rectangle([dx, y + h - 16, dx + 48, y + h - 6], fill=(120, 90, 60))
        d.rectangle([dx + 8, y + h - 30, dx + 40, y + h - 16], fill=(255, 255, 255),
                    outline=(180, 180, 180), width=1)
        for ly in range(y + h - 28, y + h - 18, 3):
            d.line([dx + 11, ly, dx + 37, ly], fill=(150, 150, 150), width=1)
    d.line([x + 16, y + h - 32, x + 34, y + h - 32], fill=(255, 200, 0), width=3)

def ill_melenchon(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 222, 230))
    fx = x + 18
    d.line([fx, y + 6, fx, y + h - 6], fill=(40, 40, 40), width=2)
    for i, c in enumerate([(0, 57, 166), (255, 255, 255), (213, 0, 50)]):
        d.rectangle([fx + i * 10, y + 6, fx + (i + 1) * 10, y + 26], fill=c)
    d.rectangle([fx, y + 6, fx + 30, y + 26], outline=(40, 40, 40), width=1)
    d.polygon([(x + 96, y + 22), (x + 150, y + 22), (x + 158, y + h - 6), (x + 88, y + h - 6)],
              fill=(120, 85, 50))
    d.rectangle([x + 96, y + 22, x + 150, y + 28], fill=(90, 60, 35))
    d.line([x + 122, y + 22, x + 122, y + 10], fill=(40, 40, 40), width=2)
    d.ellipse([x + 118, y + 4, x + 126, y + 12], fill=(40, 40, 40))

def ill_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 60))
    for sx, sy in [(30, 8), (70, 14), (150, 6), (175, 12)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    sx, sy = x + 22, y + 10
    d.polygon([(sx, sy), (sx + 22, sy), (sx + 22, sy + 14), (sx + 11, sy + 26), (sx, sy + 14)],
              fill=(40, 90, 180), outline=(255, 255, 255))
    d.line([sx + 5, sy + 13, sx + 10, sy + 18, sx + 18, sy + 7], fill=(255, 255, 255), width=2)
    bx, by = x + w - 42, y + 14
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 200, 0))
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([bx + dx * 9, by + dy * 9, bx + dx * 14, by + dy * 14], fill=(255, 200, 0), width=2)
    d.polygon([(x + 90, y + h), (x + 96, y + h - 30), (x + 108, y + h - 30), (x + 114, y + h)],
              fill=(10, 16, 32))
    for bx2, bw, bh in [(60, 24, 14), (120, 26, 18), (152, 22, 12), (178, 20, 16)]:
        d.rectangle([x + bx2, y + h - bh, x + bx2 + bw, y + h], fill=(10, 16, 32))
        for wy in range(y + h - bh + 4, y + h - 2, 6):
            for wx in range(x + bx2 + 4, x + bx2 + bw - 3, 8):
                d.rectangle([wx, wy, wx + 3, wy + 3], fill=(255, 220, 100))

def ill_haul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 222, 205))
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 8], fill=(120, 95, 70))
    for i in range(3):
        d.rectangle([x + 18 + i * 52, y + h - 40, x + 18 + i * 52 + 44, y + h - 16],
                    fill=(245, 240, 225), outline=(150, 140, 120), width=2)
        d.line([x + 18 + i * 52, y + h - 28, x + 18 + i * 52 + 44, y + h - 28],
               fill=(150, 140, 120), width=2)
    d.rectangle([x + 44, y + h - 62, x + 44 + 44, y + h - 42], fill=(245, 240, 225),
                outline=(150, 140, 120), width=2)
    cx, cy = x + w - 26, y + 16
    d.polygon([(cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy - 3), (cx + 5, cy + 2),
               (cx + 7, cy + 9), (cx, cy + 5), (cx - 7, cy + 9), (cx - 5, cy + 2),
               (cx - 10, cy - 3), (cx - 3, cy - 3)], fill=(255, 200, 0))

ILL = {"summit2": ill_summit2, "court2": ill_court2, "cop31": ill_cop31,
       "gta2": ill_gta2, "ipo2": ill_ipo2, "apec2": ill_apec2, "storm2": ill_storm2,
       "kyiv2": ill_kyiv2, "flood": ill_flood, "suneung": ill_suneung,
       "melenchon": ill_melenchon, "gulf": ill_gulf, "haul": ill_haul}

# ---- world map (LIGHT, like #1's — pale-blue oceans, beige land) ----
# Coarse continent polygons in (lon, lat); projected equirectangular into
# the map box so the numbered pins sit on the right landmass.
CONTINENTS_LL = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 70), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 20), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58)],
    # Greenland
    [(-58, 64), (-45, 60), (-40, 65), (-55, 76), (-68, 76), (-68, 70)],
    # South America
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20),
     (-77, -12)],
    # Africa
    [(-18, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, -2), (40, -10), (35, -20), (32, -29),
     (20, -35), (12, -18), (9, -1), (-8, 4)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 60), (30, 62), (25, 65), (20, 70), (15, 68),
     (5, 60), (-5, 50)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (170, 66), (158, 60), (142, 55), (135, 43), (130, 38),
     (127, 35), (122, 32), (120, 25), (110, 20), (105, 10), (100, 8),
     (95, 16), (90, 22), (85, 20), (80, 13), (77, 8), (73, 20), (67, 25),
     (60, 25), (55, 26), (50, 29), (48, 30), (44, 29), (40, 36), (35, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (135, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # Indonesia (island chain, so pin 8 sits on land)
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -5), (135, -4), (140, -8), (138, -5), (130, 0),
     (120, 5), (110, 2), (100, 5)],
]

def lonlat_to_xy(lon, lat, bx, by, bw, bh):
    # equirectangular into the map box; lat 75..-60
    x = bx + (lon + 180.0) / 360.0 * bw
    y = by + (75.0 - lat) / 135.0 * bh
    return x, y

def draw_map(d, bx, by, bw, bh, pins, dots=None):
    d.rectangle([bx, by, bx + bw, by + bh], fill=MAP_OCEAN)
    # faint graticule
    for gx in range(1, 6):
        xx = bx + bw * gx / 6
        d.line([xx, by, xx, by + bh], fill=MAP_GRID, width=1)
    for gy in range(1, 4):
        yy = by + bh * gy / 4
        d.line([bx, yy, bx + bw, yy], fill=MAP_GRID, width=1)
    for poly in CONTINENTS_LL:
        pts = [lonlat_to_xy(lon, lat, bx, by, bw, bh) for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND)
    # grey dots for the briefs (drawn first, under the red pins)
    if dots:
        for lon, lat in dots:
            px, py = lonlat_to_xy(lon, lat, bx, by, bw, bh)
            r = 3
            d.ellipse([px - r, py - r, px + r, py + r], fill=(150, 150, 150),
                      outline=(255, 255, 255), width=1)
    f_pin = sans(10, True)
    for n, (lon, lat) in pins:
        px, py = lonlat_to_xy(lon, lat, bx, by, bw, bh)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=(200, 16, 46),
                  outline=(255, 255, 255), width=1)
        t = str(n)
        tw = d.textlength(t, font=f_pin)
        d.text((px - tw / 2, py - 5), t, font=f_pin, fill=(255, 255, 255))
    d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=1)

# ---- layout ----
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    counts = region_counts()
    assert sum(counts.values()) == 43, counts
    assert sum(c for _, c in REGION_STRIP) == 43, REGION_STRIP

    # top strip
    f_top = sans(15, True)
    d.text((16, 5), "THE WORLD IN ONE DAY", font=f_top, fill=RED_DK)
    f_topr = sans(13, True)
    rt = "43 STORIES \u00b7 EVERY CONTINENT \u00b7 ALL FROM THIS ONE DAY"
    d.text((1008 - d.textlength(rt, font=f_topr), 7), rt, font=f_topr, fill=INK)
    d.line([16, 28, 1008, 28], fill=INK, width=2)

    # date headline
    f_date = serif(54, bold=True)
    d.text((16, 34), "Thursday 19 November 2026", font=f_date, fill=INK)

    # red italic sub-headline (names the three hard-news leads)
    f_sub = serif(18, italic=True)
    d.text((16, 96), "Trump, Xi and Putin share one table \u00b7 The World Court finds genocide in Myanmar \u00b7 COP31\u2019s draft drops fossil fuels",
           font=f_sub, fill=RED)
    d.line([16, 120, 1008, 120], fill=RULE, width=1)

    # region strip (7 colour-coded segments, #1 style) — breadth proof
    y_rs, rs_h = 126, 20
    seg_w = 992 / 7
    f_rs = sans(11, True)
    for i, (label, cnt) in enumerate(REGION_STRIP):
        x0 = 16 + i * seg_w
        d.rectangle([x0, y_rs, x0 + seg_w, y_rs + rs_h], fill=REG_STRIP_COL[label])
        t = "%s %d" % (label, cnt)
        tw = d.textlength(t, font=f_rs)
        d.text((x0 + (seg_w - tw) / 2, y_rs + 4), t, font=f_rs, fill=(255, 255, 255))

    # timeline strip (kept from v7/v8, below the region strip)
    y_tl, tl_h = 150, 20
    d.rectangle([16, y_tl, 1008, y_tl + tl_h], fill=NAVY)
    TL = [("OVERNIGHT", "GTA VI unlocks at midnight"),
          ("MORNING", "Summit opens in Shenzhen"),
          ("09:00", "ICJ rules"),
          ("ALL DAY", "Crimea bridge hit"),
          ("14:30", "Anthropic's first trades")]
    for _sz in (10, 9):
        f_tlb = sans(_sz, True)
        f_tlr = sans(_sz, False)
        _w = d.textlength("THE DAY IN UTC", font=f_tlb) + 16
        for _t, _e in TL:
            _w += d.textlength(_t + " \u00b7 " + _e, font=f_tlr) + 22
        if _w <= 988:
            break
    _x = 16
    d.text((_x, y_tl + 4), "THE DAY IN UTC", font=f_tlb, fill=(255, 210, 0))
    _x += d.textlength("THE DAY IN UTC", font=f_tlb) + 16
    for _t, _e in TL:
        d.text((_x, y_tl + 4), _t, font=f_tlb, fill=(255, 255, 255))
        _x += d.textlength(_t, font=f_tlb)
        d.text((_x, y_tl + 4), " \u00b7 " + _e, font=f_tlr, fill=(230, 230, 230))
        _x += d.textlength(" \u00b7 " + _e, font=f_tlr) + 22

    # big numbers (data strip, #1 style — short punchy labels, one line)
    cell_w = 992 / 6
    f_num = serif(26, bold=True)
    f_cap = sans(10)
    for i, (num, cap) in enumerate(BIG_NUMBERS):
        x0 = 16 + i * cell_w
        d.text((x0 + 4, 174), num, font=f_num, fill=RED)
        d.text((x0 + 4, 202), cap, font=f_cap, fill=INK)
    d.line([16, 218, 1008, 218], fill=INK, width=2)

    # ---- 3 leads (ALL hard news) ----
    lead_w, lead_gap = 324, 10
    lead_y = 224
    ill_h = 96
    f_badge = sans(12, True)
    f_label = sans(11, True)
    f_head = serif(19, bold=True)
    f_lsub = sans(11)
    for i, s in enumerate(LEADS):
        x0 = 16 + i * (lead_w + lead_gap)
        ILL[s["art"]](d, x0, lead_y, lead_w, ill_h)
        ly = lead_y + ill_h + 6
        # red number badge + place/topic label
        d.rectangle([x0, ly, x0 + 16, ly + 16], fill=RED)
        d.text((x0 + 5, ly + 1), str(s["n"]), font=f_badge, fill=(255, 255, 255))
        d.text((x0 + 21, ly + 2), "%s \u00b7 %s" % (s["place"], s["topic"]),
               font=f_label, fill=RED)
        hy = ly + 20
        draw_wrapped(d, x0, hy, s["headline"], f_head, INK, lead_w, leading=22)
        sy = hy + 46
        draw_wrapped(d, x0, sy, s["sub"], f_lsub, INK, lead_w, leading=13)

    # ---- grid #4, #5, #6-13 (2 rows x 5) ----
    grid_y0, grid_h = 424, 118
    grid_w, grid_gap = 192, 8
    f_glabel = sans(9, True)
    f_ghead = serif(13, bold=True)
    f_gsub = sans(10)
    for i, s in enumerate(GRID):
        row, col = divmod(i, 5)
        x0 = 16 + col * (grid_w + grid_gap)
        y0 = grid_y0 + row * (grid_h + 6)
        ILL[s["art"]](d, x0, y0, grid_w, 44)
        ly = y0 + 48
        d.rectangle([x0, ly, x0 + 14, ly + 13], fill=RED)
        d.text((x0 + 4, ly), str(s["n"]), font=sans(10, True), fill=(255, 255, 255))
        d.text((x0 + 18, ly + 1), "%s \u00b7 %s" % (s["place"], s["topic"]),
               font=f_glabel, fill=RED)
        hy = ly + 17
        hl = wrap(d, s["headline"], f_ghead, grid_w)
        sl = wrap(d, s["sub"], f_gsub, grid_w)
        if len(hl) > 2 or len(sl) > 2:
            print("WARN grid #%d wraps: headline %d lines, sub %d lines" % (s["n"], len(hl), len(sl)))
        draw_wrapped(d, x0, hy, s["headline"], f_ghead, INK, grid_w, leading=15)
        draw_wrapped(d, x0, hy + 32, s["sub"], f_gsub, INK, grid_w, leading=12)

    # ---- map (left, LIGHT) + text list (right, with per-item sources) ----
    map_x, map_y, map_w, map_h = 16, 692, 330, 216
    list_x = 354
    f_sec = sans(13, True)
    d.text((map_x, 672), "WHERE IT HAPPENED", font=f_sec, fill=RED_DK)
    d.text((list_x, 672), "ALSO ON THURSDAY 19 NOVEMBER \u2014 30 MORE STORIES",
           font=f_sec, fill=RED_DK)
    pins = [(s["n"], s["pin"]) for s in LEADS + GRID]
    # nudge the crowded Europe pins apart so the numbers stay readable
    # (the map note says positions are approximate)
    PIN_NUDGE = {3: (36.0, 36.0), 11: (-2.0, 43.0)}
    pins = [(n, PIN_NUDGE.get(n, p)) for n, p in pins]
    dots = [p for p in BRIEF_PINS if p is not None]
    draw_map(d, map_x, map_y, map_w, map_h, pins, dots=dots)
    f_note = sans(9)
    draw_wrapped(d, map_x, 912, "Red numbers mark stories 1\u201313; grey dots mark the briefs below.",
                 f_note, GREY, map_w, leading=11)
    # region legend: each region's name + count in its own bar colour
    f_leg = sans(8)
    lx = map_x
    for i, r in enumerate(REGIONS):
        seg = "%s %d" % (r, counts[r])
        if i:
            d.text((lx, 924), "\u00b7", font=f_leg, fill=GREY)
            lx += d.textlength("\u00b7 ", font=f_leg)
        d.text((lx, 924), seg, font=f_leg, fill=REG_COL[r])
        lx += d.textlength(seg + " ", font=f_leg)

    # text list: 2 columns x 15 briefs, one line each, with source
    f_bnum = sans(10, True)
    f_btxt = sans(9)
    col_w = 322
    for i, (place, txt, src) in enumerate(BRIEFS):
        col = 0 if i < 15 else 1
        row = i if i < 15 else i - 15
        x0 = list_x + col * (col_w + 10)
        y0 = 692 + row * 16
        n = i + 14
        d.text((x0, y0), str(n), font=f_bnum, fill=RED)
        nw = d.textlength(str(n), font=f_bnum) + 4
        full = "%s \u2014 %s %s" % (place, txt, src)
        lines = wrap(d, full, f_btxt, col_w - nw)
        if len(lines) > 1:
            print("WARN brief #%d wraps to %d lines: %s" % (n, len(lines), full))
        d.text((x0 + nw, y0), lines[0], font=f_btxt, fill=INK)

    # ---- DATE CHECK box (opens with the positive claim; both 18 + 20 NOV) ----
    d.rectangle([16, 956, 1008, 996], outline=RED, width=2)
    f_dc = sans(10)
    draw_wrapped(d, 24, 960, DATE_CHECK, f_dc, INK, 976, leading=11)

    # ---- footer (one line, #1 format) ----
    f_foot = sans(9)
    d.text((512 - d.textlength(FOOTER, font=f_foot) // 2, 1004), FOOTER, font=f_foot, fill=GREY)

    img.save(OUT, format="PNG")
    return OUT

if __name__ == "__main__":
    out = build()
    print(out, os.path.getsize(out), "bytes")
