"""
generates three transparent PNG star tile layers using the DawnBringer-32 palette.
layer 1: small/dense (far), layer 2: medium (mid), layer 3: large/sparse (near)
"""

import random
from PIL import Image, ImageDraw
from pathlib import Path

DB32 = [
    (0,   0,   0),   (34,  32,  52),  (69,  40,  60),  (102, 57,  49),
    (143, 86,  59),  (223, 113, 38),  (217, 160, 102), (238, 195, 154),
    (251, 242, 54),  (153, 229, 80),  (106, 190, 48),  (55,  148, 110),
    (75,  105, 47),  (82,  75,  36),  (50,  60,  57),  (63,  63,  116),
    (48,  96,  130), (91,  110, 225), (99,  155, 255), (95,  205, 228),
    (203, 219, 252), (255, 255, 255), (155, 173, 183), (132, 126, 135),
    (105, 106, 106), (89,  86,  82),  (118, 66,  138), (172, 50,  50),
    (217, 87,  99),  (215, 123, 186), (143, 151, 74),  (138, 111, 48),
]

# skip near-black colors for visibility against dark backgrounds
USABLE = [c for c in DB32 if sum(c) > 120]

SIZE   = 1024
OUTPUT = Path('src/images')
OUTPUT.mkdir(parents=True, exist_ok=True)

LAYERS = [
    # (filename,         dot_count, dot_size_range)
    ('stars-far.png',    55,        (1, 1)),
    ('stars-mid.png',    30,        (2, 3)),
    ('stars-near.png',   14,        (4, 6)),
]

random.seed(42)  # reproducible -- re-run to get the same tiles

for filename, count, (min_size, max_size) in LAYERS:
    img  = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for _ in range(count):
        x    = random.randint(0, SIZE - 1)
        y    = random.randint(0, SIZE - 1)
        size = random.randint(min_size, max_size)
        r, g, b = random.choice(USABLE)
        alpha = random.randint(140, 220)
        draw.rectangle([x, y, x + size - 1, y + size - 1], fill=(r, g, b, alpha))

    out = OUTPUT / filename
    img.save(out, 'PNG')
    print(f"  {out}  ({count} dots, {min_size}-{max_size}px)")

print("done.")
