"""Generate deterministic, geospatial-themed SVG cover art for projects
that have no screenshot. Same title always yields the same artwork."""
import hashlib, math, os, re

W, H = 640, 440
OUT = 'images/covers'
os.makedirs(OUT, exist_ok=True)


class Rng:
    """Small deterministic PRNG seeded from the project title."""

    def __init__(self, seed):
        self.x = int(hashlib.sha256(seed.encode()).hexdigest()[:16], 16) or 1

    def next(self):
        self.x = (self.x * 6364136223846793005 + 1442695040888963407) % (2 ** 64)
        return self.x / 2 ** 64

    def uniform(self, a, b):
        return a + (b - a) * self.next()

    def randint(self, a, b):
        return int(self.uniform(a, b + 1))


def contours(r):
    """Stacked topographic contour lines."""
    out = []
    for i in range(11):
        y0 = 60 + i * 34
        amp = r.uniform(10, 30)
        ph = r.uniform(0, 6.3)
        pts = []
        for x in range(0, W + 20, 20):
            y = y0 + amp * math.sin(x / r.uniform(70, 130) + ph) + amp * 0.4 * math.sin(x / 47 + ph * 2)
            pts.append(f'{x},{y:.1f}')
        op = 0.10 + 0.32 * (1 - abs(i - 5) / 6)
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#fff" '
                   f'stroke-width="{r.uniform(1, 2.4):.1f}" opacity="{op:.2f}"/>')
    return '\n'.join(out)


def raster(r):
    """Pixel/raster grid with a hot spot — reads as gridded EO data."""
    out, cell = [], 40
    cx, cy = r.uniform(0.25, 0.75) * W, r.uniform(0.3, 0.7) * H
    for gx in range(0, W, cell):
        for gy in range(0, H, cell):
            d = math.hypot(gx + cell / 2 - cx, gy + cell / 2 - cy) / (W * 0.55)
            op = max(0.04, (1 - d) * r.uniform(0.35, 0.6))
            out.append(f'<rect x="{gx + 2}" y="{gy + 2}" width="{cell - 4}" height="{cell - 4}" '
                       f'rx="3" fill="#fff" opacity="{op:.2f}"/>')
    return '\n'.join(out)


def basin(r):
    """Dendritic river network."""
    out = []

    def branch(x, y, ang, ln, depth, wdt):
        if depth == 0 or ln < 12:
            return
        x2 = x + math.cos(ang) * ln
        y2 = y + math.sin(ang) * ln
        out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                   f'stroke="#fff" stroke-width="{wdt:.1f}" stroke-linecap="round" '
                   f'opacity="{0.15 + 0.06 * depth:.2f}"/>')
        for s in (-1, 1):
            branch(x2, y2, ang + s * r.uniform(0.35, 0.75), ln * r.uniform(0.6, 0.78),
                   depth - 1, max(0.8, wdt * 0.7))

    branch(W * 0.5, H + 10, -math.pi / 2, 110, 6, 6)
    return '\n'.join(out)


def hexbin(r):
    """Hexagonal binning grid."""
    out, s = [], 30
    for row in range(-1, H // int(s * 1.5) + 2):
        for col in range(-1, W // int(s * 1.75) + 2):
            cx = col * s * 1.74 + (s * 0.87 if row % 2 else 0)
            cy = row * s * 1.5
            pts = ' '.join(f'{cx + s * math.cos(math.pi / 6 + k * math.pi / 3):.1f},'
                           f'{cy + s * math.sin(math.pi / 6 + k * math.pi / 3):.1f}' for k in range(6))
            out.append(f'<polygon points="{pts}" fill="#fff" opacity="{r.uniform(0.03, 0.4):.2f}" '
                       f'stroke="#fff" stroke-opacity="0.10"/>')
    return '\n'.join(out)


def flow(r):
    """Directional flow field — pipelines, streaming, movement."""
    out = []
    for i in range(26):
        y = r.uniform(20, H - 20)
        x = r.uniform(-40, W * 0.6)
        ln = r.uniform(80, 260)
        cur = r.uniform(-40, 40)
        out.append(f'<path d="M{x:.0f},{y:.0f} q{ln / 2:.0f},{cur:.0f} {ln:.0f},0" fill="none" '
                   f'stroke="#fff" stroke-width="{r.uniform(1, 3):.1f}" stroke-linecap="round" '
                   f'opacity="{r.uniform(0.10, 0.45):.2f}"/>')
        out.append(f'<circle cx="{x + ln:.0f}" cy="{y:.0f}" r="{r.uniform(2, 4):.1f}" '
                   f'fill="#fff" opacity="{r.uniform(0.3, 0.7):.2f}"/>')
    return '\n'.join(out)


def points(r):
    """Scattered sample points with proportional symbols."""
    out = []
    for _ in range(34):
        cx, cy = r.uniform(30, W - 30), r.uniform(30, H - 30)
        rad = r.uniform(4, 26)
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad:.0f}" fill="#fff" '
                   f'opacity="{r.uniform(0.08, 0.30):.2f}" stroke="#fff" stroke-opacity="0.25"/>')
    return '\n'.join(out)


MOTIFS = {'contours': contours, 'raster': raster, 'basin': basin,
          'hexbin': hexbin, 'flow': flow, 'points': points}

# palette pairs, all rooted in the site's teal
PALETTES = [('#0b3b39', '#0f766e'), ('#08302f', '#14857a'), ('#0d4f47', '#0d9488'),
            ('#062b2a', '#115e59'), ('#124b45', '#12a594')]


def build(title, motif, slug):
    r = Rng(title)
    a, b = PALETTES[Rng(title + 'p').randint(0, len(PALETTES) - 1)]
    art = MOTIFS[motif](r)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/>
    </linearGradient>
    <clipPath id="c"><rect width="{W}" height="{H}"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <g clip-path="url(#c)">
{art}
  </g>
</svg>
'''
    open(f'{OUT}/{slug}.svg', 'w', encoding='utf-8').write(svg)
    return f'{OUT}/{slug}.svg'


PROJECTS = [
    ('GeoAI Drought Modelling Framework', 'contours', 'geoai-drought-framework'),
    ('Basin Geomorphology & Hydrological Drought', 'basin', 'basin-geomorphology-drought'),
    ('GeoAI Flood Prediction', 'contours', 'geoai-flood-prediction'),
    ('GeoAI Orthophoto LULC Classification', 'raster', 'geoai-orthophoto-lulc'),
    ('Land Use & Hydrological Drought', 'basin', 'landuse-hydrological-drought'),
    ('Population Growth Hotspots', 'points', 'population-growth-hotspots'),
    ('Crop Classification Amini', 'raster', 'crop-classification-amini'),
    ('Ground-Level NO2 Estimation', 'points', 'no2-estimation'),
    ('Tocantins Soil Carbon Prediction', 'hexbin', 'tocantins-soil-carbon'),
    ('Airflow Forex ETL Pipeline', 'flow', 'airflow-forex-etl'),
    ('Uber Data Analytics ETL', 'flow', 'uber-analytics-etl'),
    ('ArcGIS Feature Service Connector', 'flow', 'arcgis-connector'),
    ('Perth POI Ingestion Pipeline', 'points', 'perth-poi-etl'),
    ('Real-Time Data Streaming Pipeline', 'flow', 'realtime-streaming'),
    ('Spatial Analysis with DuckDB', 'hexbin', 'duckdb-spatial'),
    ('Okomu Enterprise Farm Intelligence Platform', 'hexbin', 'okomu-farm-intelligence'),
]

for title, motif, slug in PROJECTS:
    print('wrote', build(title, motif, slug))
