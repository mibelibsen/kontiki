# -*- coding: utf-8 -*-
"""QR-koder uden afhaengigheder.

Ren Python, saa den virker i en frisk session uden pip. Understoetter
byte-tilstand, version 1-10 (op til 271 tegn ved fejlniveau L, 122 ved M)
og alle fire fejlniveauer. Det raekker rigeligt til en webadresse.

Brug:
    import sys; sys.path.insert(0, 'claude')
    import qr
    svg = qr.svg('https://www.mibelibsen.space/u/anna', ec='M', mm=60)
    m, version, maske = qr.matrix('tekst', ec='Q')   # liste af lister, 1 = moerk

Koderen er krydstjekket mod biblioteket segno (ISO 18004): hver kombination
af version 1-10 og fejlniveau giver moduler, der er identiske bit for bit.
Koer `python3 claude/qr.py` for at gentage tjekket (kraever `pip install segno`).
"""

# ------------------------------------------------------------------ tabeller
# Fejlrettelseskodeord pr. blok og antal blokke, version 1-10 (ISO 18004,
# tabel 9). Indeks 0 er version 1.
_EC_PR_BLOK = {
    'L': [7, 10, 15, 20, 26, 18, 20, 24, 30, 18],
    'M': [10, 16, 26, 18, 24, 16, 18, 22, 22, 26],
    'Q': [13, 22, 18, 26, 18, 24, 18, 22, 20, 24],
    'H': [17, 28, 22, 16, 22, 28, 26, 26, 24, 28],
}
_BLOKKE = {
    'L': [1, 1, 1, 1, 1, 2, 2, 2, 2, 4],
    'M': [1, 1, 1, 2, 2, 4, 4, 4, 5, 5],
    'Q': [1, 1, 2, 2, 4, 4, 6, 6, 8, 8],
    'H': [1, 1, 2, 4, 4, 4, 5, 6, 8, 8],
}
_EC_BITS = {'L': 1, 'M': 0, 'Q': 3, 'H': 2}
MAKS_VERSION = 10


def _raa_moduler(v):
    """Antal moduler til data + fejlrettelse, naar funktionsmoenstrene er trukket fra."""
    n = (16 * v + 128) * v + 64
    if v >= 2:
        a = v // 7 + 2
        n -= (25 * a - 10) * a - 55
        if v >= 7:
            n -= 36
    return n


def _datakodeord(v, ec):
    return _raa_moduler(v) // 8 - _EC_PR_BLOK[ec][v - 1] * _BLOKKE[ec][v - 1]


def kapacitet(v, ec):
    """Antal bytes der kan ligge i version v ved fejlniveau ec."""
    tael = 8 if v <= 9 else 16
    return (_datakodeord(v, ec) * 8 - 4 - tael) // 8


# ------------------------------------------------------------- GF(256) og RS
def _gf_mul(x, y):
    z = 0
    for i in range(7, -1, -1):
        z = (z << 1) ^ ((z >> 7) * 0x11D)
        z ^= ((y >> i) & 1) * x
    return z


def _rs_generator(grad):
    g = [0] * (grad - 1) + [1]
    rod = 1
    for _ in range(grad):
        for j in range(len(g)):
            g[j] = _gf_mul(g[j], rod)
            if j + 1 < len(g):
                g[j] ^= g[j + 1]
        rod = _gf_mul(rod, 2)
    return g


def _rs_rest(data, g):
    r = [0] * len(g)
    for b in data:
        faktor = b ^ r.pop(0)
        r.append(0)
        for i, k in enumerate(g):
            r[i] ^= _gf_mul(k, faktor)
    return r


# ------------------------------------------------------------------ bitstroem
def _kodeord(tekst, v, ec):
    data = tekst.encode('utf-8')
    tael = 8 if v <= 9 else 16
    bits = []

    def put(val, n):
        for i in range(n - 1, -1, -1):
            bits.append((val >> i) & 1)

    put(0b0100, 4)                       # byte-tilstand
    put(len(data), tael)
    for b in data:
        put(b, 8)
    n_kap = _datakodeord(v, ec) * 8
    assert len(bits) <= n_kap, 'teksten er for lang til versionen'
    put(0, min(4, n_kap - len(bits)))    # terminator
    while len(bits) % 8:
        bits.append(0)
    pad = (0xEC, 0x11)
    i = 0
    while len(bits) < n_kap:
        put(pad[i % 2], 8)
        i += 1
    return [int(''.join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]


def _flet(kodeord, v, ec):
    """Deler i blokke, regner fejlrettelse og fletter som standarden foreskriver."""
    n_blok = _BLOKKE[ec][v - 1]
    ec_len = _EC_PR_BLOK[ec][v - 1]
    raa = _raa_moduler(v) // 8
    n_korte = n_blok - raa % n_blok
    kort = raa // n_blok
    g = _rs_generator(ec_len)
    blokke, k = [], 0
    for i in range(n_blok):
        laengde = kort - ec_len + (0 if i < n_korte else 1)
        dat = kodeord[k:k + laengde]
        k += laengde
        ecc = _rs_rest(dat, g)
        if i < n_korte:
            dat = dat + [None]              # hul, saa alle blokke er lige lange
        blokke.append(dat + ecc)
    assert k == len(kodeord)
    ud = []
    for i in range(len(blokke[0])):
        for j in range(n_blok):
            if blokke[j][i] is not None:
                ud.append(blokke[j][i])
    return ud


# ------------------------------------------------------------------- matrix
def _funktionsmoenstre(v):
    """Returnerer (moduler, funktion) — funktion markerer de faste felter."""
    n = v * 4 + 17
    m = [[0] * n for _ in range(n)]
    f = [[False] * n for _ in range(n)]

    def saet(x, y, moerk):
        m[y][x] = 1 if moerk else 0
        f[y][x] = True

    for i in range(n):                                   # timing
        saet(6, i, i % 2 == 0)
        saet(i, 6, i % 2 == 0)
    for cx, cy in ((3, 3), (n - 4, 3), (3, n - 4)):      # soegemoenstre + separator
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                x, y = cx + dx, cy + dy
                if 0 <= x < n and 0 <= y < n:
                    d = max(abs(dx), abs(dy))
                    saet(x, y, d != 2 and d != 4)
    pos = _justering(v)                                  # justeringsmoenstre
    for i, py in enumerate(pos):
        for j, px in enumerate(pos):
            if (i == 0 and j == 0) or (i == 0 and j == len(pos) - 1) \
                    or (i == len(pos) - 1 and j == 0):
                continue
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    saet(px + dx, py + dy, max(abs(dx), abs(dy)) != 1)
    # reserver felterne til formatinformation (skrives efter maskevalget)
    for i in range(9):
        if i != 6:                                       # ikke hen over timing
            saet(8, i, False); saet(i, 8, False)
    for i in range(8):
        saet(n - 1 - i, 8, False); saet(8, n - 1 - i, False)
    if v >= 7:
        _versionsinfo(m, f, v)
    return m, f


def _justering(v):
    if v == 1:
        return []
    antal = v // 7 + 2
    n = v * 4 + 17
    skridt = (v * 4 + antal * 2 + 1) // (antal * 2 - 2) * 2
    pos, p = [6], n - 7
    for _ in range(antal - 1):
        pos.insert(1, p)
        p -= skridt
    return pos


def _versionsinfo(m, f, v):
    n = v * 4 + 17
    rest = v
    for _ in range(12):
        rest = (rest << 1) ^ ((rest >> 11) * 0x1F25)
    bits = v << 12 | rest
    for i in range(18):
        bit = (bits >> i) & 1
        a, b = n - 11 + i % 3, i // 3
        m[b][a] = bit; f[b][a] = True
        m[a][b] = bit; f[a][b] = True


def _formatinfo(m, f, ec, maske):
    n = len(m)
    data = _EC_BITS[ec] << 3 | maske
    rest = data
    for _ in range(10):
        rest = (rest << 1) ^ ((rest >> 9) * 0x537)
    bits = (data << 10 | rest) ^ 0x5412

    def bit(i):
        return (bits >> i) & 1

    for i in range(6):
        m[i][8] = bit(i)
    m[7][8] = bit(6)
    m[8][8] = bit(7)
    m[8][7] = bit(8)
    for i in range(9, 15):
        m[8][14 - i] = bit(i)
    for i in range(8):
        m[8][n - 1 - i] = bit(i)
    for i in range(8, 15):
        m[n - 15 + i][8] = bit(i)
    m[n - 8][8] = 1                      # det altid moerke modul


def _laeg_data(m, f, kodeord):
    n = len(m)
    bits = [(b >> (7 - k)) & 1 for b in kodeord for k in range(8)]
    i = 0
    hoejre = n - 1
    while hoejre >= 1:
        if hoejre == 6:
            hoejre = 5
        opad = ((hoejre + 1) & 2) == 0
        for lodret in range(n):
            y = n - 1 - lodret if opad else lodret
            for j in range(2):
                x = hoejre - j
                if not f[y][x] and i < len(bits):
                    m[y][x] = bits[i]
                    i += 1
        hoejre -= 2
    assert i == len(bits)


_MASKER = [
    lambda i, j: (i + j) % 2 == 0,
    lambda i, j: i % 2 == 0,
    lambda i, j: j % 3 == 0,
    lambda i, j: (i + j) % 3 == 0,
    lambda i, j: (i // 2 + j // 3) % 2 == 0,
    lambda i, j: (i * j) % 2 + (i * j) % 3 == 0,
    lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0,
    lambda i, j: ((i + j) % 2 + (i * j) % 3) % 2 == 0,
]


def _masker(m, f, k):
    n = len(m)
    mk = _MASKER[k]
    for y in range(n):
        for x in range(n):
            if not f[y][x] and mk(y, x):
                m[y][x] ^= 1


def _straf(m):
    """Strafpoint efter ISO 18004, afsnit 7.8.3 — regnet som segno goer det,
    saa maskevalget kan krydstjekkes bit for bit. I regel 3 taeller
    stillezonen uden om symbolet som lys, og hvert moenster taeller een gang."""
    n = len(m)
    s = 0

    def linje(vals):
        p = 0
        i = 0                                           # regel 1: 5+ ens i traek
        while i < n:
            j = i
            while j < n and vals[j] == vals[i]:
                j += 1
            if j - i >= 5:
                p += 3 + (j - i - 5)
            i = j
        t = ''.join(map(str, vals))                     # regel 3: 1011101
        idx = t.find('1011101')
        while idx != -1:
            slut = idx + 7
            if idx in (0, n - 7) or '1' not in t[max(idx - 4, 0):idx] \
                    or '1' not in t[slut:slut + 4]:
                p += 40
            else:
                slut = idx + 4
            idx = t.find('1011101', slut)
        return p

    for y in range(n):
        s += linje(m[y])
    for x in range(n):
        s += linje([m[y][x] for y in range(n)])
    for y in range(n - 1):                              # regel 2: 2x2-blokke
        for x in range(n - 1):
            if m[y][x] == m[y][x + 1] == m[y + 1][x] == m[y + 1][x + 1]:
                s += 3
    moerke = sum(map(sum, m))                           # regel 4: balance
    total = n * n
    s += 10 * (abs(moerke * 100 - total * 50) // (5 * total))
    return s


# --------------------------------------------------------------- offentligt
def version_til(tekst, ec='M'):
    n = len(tekst.encode('utf-8'))
    for v in range(1, MAKS_VERSION + 1):
        if kapacitet(v, ec) >= n:
            return v
    raise ValueError(f'teksten fylder {n} bytes — mere end version {MAKS_VERSION} '
                     f'rummer ved niveau {ec} ({kapacitet(MAKS_VERSION, ec)})')


def matrix(tekst, ec='M', version=None, maske=None):
    """Returnerer (moduler, version, maske). moduler[y][x] er 1 for moerk."""
    ec = ec.upper()
    v = version or version_til(tekst, ec)
    assert 1 <= v <= MAKS_VERSION
    kodeord = _flet(_kodeord(tekst, v, ec), v, ec)
    bedst = None
    for k in ([maske] if maske is not None else range(8)):
        m, f = _funktionsmoenstre(v)
        _laeg_data(m, f, kodeord)
        _masker(m, f, k)
        _formatinfo(m, f, ec, k)
        p = _straf(m)
        if bedst is None or p < bedst[0]:
            bedst = (p, k, m)
    return bedst[2], v, bedst[1]


def svg(tekst, ec='M', mm=50, stille=4, farve='#000', baggrund='#fff', attrs=''):
    """QR-koden som SVG med fire modulers stillezone hele vejen rundt.

    Modulerne tegnes som een path af hele kvadrater, saa der ikke opstaar
    hvide streger mellem dem ved skalering."""
    m, v, k = matrix(tekst, ec)
    n = len(m)
    N = n + 2 * stille
    d = []
    for y in range(n):
        x = 0
        while x < n:
            if m[y][x]:
                x0 = x
                while x < n and m[y][x]:
                    x += 1
                d.append(f'M{x0 + stille} {y + stille}h{x - x0}v1h-{x - x0}z')
            else:
                x += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}" '
            f'width="{mm}mm" height="{mm}mm" shape-rendering="crispEdges" '
            f'role="img" aria-label="QR-kode til {tekst}" {attrs}>'
            f'<rect width="{N}" height="{N}" fill="{baggrund}"/>'
            f'<path d="{"".join(d)}" fill="{farve}"/></svg>')


# ----------------------------------------------------------------- selvtest
def _selvtest():
    """Krydstjek mod segno og afkodning med zxing-cpp.

    segno skriver et ekstra nul-kodeord, naar terminatoren ender praecis paa en
    bytegraense (det goer den altid i byte-tilstand). Standarden (ISO 18004,
    7.4.10) siger, at der kun fyldes op TIL graensen, saa den del af segno
    erstattes med standardens adfaerd, foer matricerne sammenlignes."""
    import segno
    from segno import encoder

    def standard_padding(buff, version, length):
        buff.extend([0] * ((8 - length % 8) % 8))
    encoder.write_padding_bits = standard_padding

    tekster = ['https://www.mibelibsen.space/u/anna', 'Kontiki 9. klasse · æøå',
               'a' * 20, 'abc', 'https://docs.google.com/forms/d/e/1FAIpQLSdX9x_'
               'abcdefghijklmnopqrstuvwxyz0123456789/viewform?usp=pp_url&'
               'entry.1234567890=S%C3%B8ren+%C3%98stergaard']
    antal = 0
    for ec in 'LMQH':
        for v in range(1, MAKS_VERSION + 1):
            for t in tekster:
                # segno koder æøå som Latin-1; her skrives UTF-8, som telefoner
                # laeser. Ikke-ASCII tjekkes derfor kun ved afkodningen nedenfor.
                if len(t.encode()) > kapacitet(v, ec) or not t.isascii():
                    continue
                for maske in range(8):
                    m, _, _ = matrix(t, ec, version=v, maske=maske)
                    s = segno.make(t, error=ec.lower(), version=v, mask=maske,
                                   mode='byte', boost_error=False)
                    ref = [[int(c) for c in row] for row in s.matrix]
                    assert m == ref, f'afviger: version {v} niveau {ec} maske {maske}'
                    antal += 1
                # strafpointene skal vaere segnos, maske for maske; selve valget
                # kan afvige, fordi segno vurderer matricen uden formatinformation
                for maske in range(8):
                    m, _, _ = matrix(t, ec, version=v, maske=maske)
                    ref = sum(encoder.mask_scores([bytearray(r) for r in m],
                                                  len(m), len(m)))
                    assert _straf(m) == ref, f'strafpoint v{v} {ec} maske {maske}'
    print(f'qr.py: {antal} koder identiske med segno, version 1-{MAKS_VERSION}, '
          f'alle niveauer og masker, samme strafpoint')
    try:
        import zxingcpp, numpy
    except ImportError:
        print('qr.py: zxing-cpp ikke installeret, springer afkodning over')
        return
    laest = 0
    for ec in 'LMQH':
        for t in tekster:
            if len(t.encode()) > kapacitet(MAKS_VERSION, ec):
                continue
            m, v, _ = matrix(t, ec)
            n = len(m)
            px = numpy.full(((n + 8) * 6, (n + 8) * 6), 255, dtype=numpy.uint8)
            for y in range(n):
                for x in range(n):
                    if m[y][x]:
                        px[(y + 4) * 6:(y + 5) * 6, (x + 4) * 6:(x + 5) * 6] = 0
            r = zxingcpp.read_barcode(px)
            assert r is not None and r.text == t, f'kunne ikke laese v{v} {ec}: {t!r}'
            laest += 1
    print(f'qr.py: {laest} koder laest tilbage med zxing-cpp, tekst for tekst')


if __name__ == '__main__':
    _selvtest()
