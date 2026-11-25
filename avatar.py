# 32x32 piksel avatar: beyaz saçlı, sarı kulaklıklı karakter, mor gece gökyüzü.
import sys, math, random
from PIL import Image

N = 32
G = [['.'] * N for _ in range(N)]
def put(x, y, c):
    if 0 <= x < N and 0 <= y < N: G[y][x] = c
def get(x, y):
    return G[y][x] if 0 <= x < N and 0 <= y < N else ""
def ell(cx, cy, rx, ry, c, test=None):
    for y in range(N):
        for x in range(N):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1 and (test is None or test(x, y)): put(x, y, c)
def outline(fill_chars, oc='K', only_empty=True):
    pts = []
    for y in range(N):
        for x in range(N):
            if G[y][x] in fill_chars: continue
            if only_empty and G[y][x] != '.': continue
            if any(get(x + dx, y + dy) in fill_chars for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): pts.append((x, y))
    for x, y in pts: put(x, y, oc)
def sprite(x0, y0, rows):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != ' ': put(x0 + i, y0 + j, ch)

# --- hoodie / shoulders
for y in range(24, N):
    t = y - 24
    half = 7 + t * 2 if t < 4 else 15 + (t - 4)
    for x in range(int(15.5 - half), int(15.5 + half) + 1): put(x, y, 'C')
for y in range(25, N):  # shading on the sides
    for x in range(N):
        if G[y][x] == 'C' and (x < 9 or x > 22): put(x, y, 'c')
outline('Cc')
# neck + collar
for y in range(21, 27):
    for x in range(13, 19): put(x, y, 's' if y < 23 else 'S')
sprite(12, 26, ['K    K', ' K  K ', '  KK  '])            # collar V
sprite(11, 27, ['L', 'L', 'l']); sprite(20, 27, ['L', 'L', 'l'])  # hoodie strings

# --- back hair
ell(15.5, 12.5, 10.2, 10.0, 'H')
for y in range(N):
    for x in range(N):
        if G[y][x] == 'H' and y > 15: put(x, y, 'h')
outline('Hh')

# --- face
fw = {10: 6.6, 11: 6.6, 12: 6.6, 13: 6.6, 14: 6.6, 15: 6.6, 16: 6.6, 17: 6.4, 18: 6.1, 19: 5.6, 20: 4.9, 21: 4.0, 22: 2.8, 23: 1.4}
for y, w in fw.items():
    for x in range(N):
        if abs(x + .5 - 16) <= w: put(x, y, 'S')
# face outline (sides + chin)
for y in range(10, 25):
    for x in range(N):
        if G[y][x] != 'S' and G[y][x] not in 'Kss' and any(get(x + dx, y + dy) == 'S' for dx, dy in ((1,0),(-1,0),(0,-1))):
            if y >= 12: put(x, y, 'K')
for y in range(18, 22):  # soft shade under the cheeks
    for x in (10, 21):
        if get(x, y) == 'S': put(x, y, 's')

# --- bangs (spiky, over the forehead)
bang_bottom = [12, 13, 14, 13, 13, 13, 15, 14, 13, 13, 14, 13, 12]   # per 2-px column from x=3
for i, b in enumerate(bang_bottom):
    for k in range(2):
        x = 3 + i * 2 + k
        top = 3
        for y in range(top, b + (1 if k == 0 else 0)):
            inside = ((x + .5 - 15.5) / 10.2) ** 2 + ((y + .5 - 12.5) / 10.0) ** 2 <= 1
            if get(x, y) in ('.', 'S', 'H', 'h', 'K') and inside: put(x, y, 'H')
        yb = b + (1 if k == 0 else 0)
        if 9 <= x <= 22 and get(x, yb) == 'S': put(x, yb, 'k')   # dark tip line under the bang
for y in range(4, 16):
    for x in range(N):
        if G[y][x] == 'H' and get(x, y + 1) in ('S', 'k'): put(x, y, 'h')   # underside shade of each spike
# a few strand lines and a highlight band
for x, y in ((9, 7), (12, 6), (19, 6), (22, 7), (15, 8), (16, 9)): put(x, y, 'h')
for x in range(10, 22):
    if get(x, 5) == 'H' and x % 3 != 0: put(x, 5, 'W')
outline('HhW', only_empty=True)

# --- side locks hanging beside the face
for y in range(13, 24):
    for x in (8, 9, 22, 23):
        if y > 21 and x in (8, 23): continue
        put(x, y, 'h' if y > 18 else 'H')
for y in range(13, 24):
    for x in (7, 24):
        if y <= 21: put(x, y, 'K')
for x in (8, 9, 22, 23):
    y = 22 if x in (9, 22) else 22
    if get(x, 24) not in ('S', 's'): put(x, 24 if x in (9, 22) else 22, 'K')
# --- eyes (big, violet iris, white highlight)
EYE = ['KKKK',
       'WiIi',
       'iIIi',
       ' jj ']
sprite(10, 16, EYE); sprite(18, 16, EYE)
put(9, 15, 'K'); put(22, 15, 'K')          # small outer lash flicks
# blush, nose, mouth
for x, y in ((10, 20), (11, 20), (20, 20), (21, 20)): put(x, y, 'B')
put(16, 20, 's')
sprite(15, 22, ['MM'])

# --- headphones: band over the head, cups at the ears
for y in range(0, 14):
    for x in range(N):
        d = math.hypot(x + .5 - 15.5, (y + .5 - 13.2) * 1.02)
        if y + .5 > 13.2: continue
        if 11.1 < d <= 12.2: put(x, y, 'K')
        elif 9.9 < d <= 11.1: put(x, y, 'Y')
        elif 9.0 < d <= 9.9: put(x, y, 'y')
for x0 in (2, 25):
    sprite(x0, 11, [' KKK ',
                    'KPPPK',
                    'KPpPK',
                    'KPpPK',
                    'KPpPK',
                    'KPPPK',
                    'KPPPK',
                    'KPPPK',
                    ' KKK '])
    side = x0 if x0 < 15 else x0 + 4
    for y in range(12, 19): put(side, y, 'Y')     # yellow rim on the outer side
    put(side, 11, 'y'); put(side, 19, 'y')
# mic boom from the right cup
for x, y in ((24, 19), (23, 20), (22, 21), (21, 22)): put(x, y, 'K')
put(20, 22, 'p')

PAL = {'K': (20, 14, 34), 'k': (120, 98, 140), 'H': (244, 242, 252), 'h': (196, 190, 222), 'W': (255, 255, 255),
       'S': (255, 233, 222), 's': (238, 196, 186), 'B': (250, 160, 170), 'M': (196, 92, 104),
       'i': (124, 92, 255), 'I': (58, 34, 140), 'j': (184, 164, 255),
       'Y': (248, 202, 40), 'y': (190, 140, 16), 'P': (44, 40, 58), 'p': (88, 82, 110),
       'C': (36, 30, 58), 'c': (26, 21, 44), 'L': (232, 228, 244), 'l': (170, 164, 196)}
sky = [(13, 7, 30), (20, 11, 46), (30, 16, 64), (42, 21, 84), (56, 27, 104)]
random.seed(11)
stars = {(random.randrange(N), random.randrange(22)) for _ in range(16)}
img = Image.new('RGB', (N, N)); px = img.load()
for y in range(N):
    for x in range(N):
        c = G[y][x]
        if c == '.':
            t = y / N * (len(sky) - 1); k = int(t); f = t - k
            bay = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]][y % 4][x % 4] / 16
            col = sky[min(len(sky) - 1, k + (1 if f > bay else 0))]
            if (x, y) in stars: col = (236, 222, 255) if (x + y) % 3 else (160, 132, 230)
            px[x, y] = col
        else:
            px[x, y] = PAL[c]
img.save(sys.argv[1])
olcek = int(sys.argv[3]) if len(sys.argv) > 3 else 16
olcek = max(1, min(64, olcek))
img.resize((N * olcek, N * olcek), Image.NEAREST).save(sys.argv[2])
open(sys.argv[1] + '.txt', 'w').write('\n'.join(''.join(r) for r in G))
print('ok')
