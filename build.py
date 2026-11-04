"""Gera os SVGs estáticos/animados do perfil. Edite CONFIG e rode: python build.py"""
import html

CONFIG = {
    "nome": "SEU NOME",
    "subtitulo": "DESENVOLVEDOR FULLSTACK EM FORMAÇÃO",
    "exp": 50,  # 0-100
    "atributos": [  # (nome, nível de 0 a 5)
        ("PYTHON", 4), ("DADOS", 4), ("HARDWARE", 3),
        ("LÓGICA", 2), ("GIT E GITHUB", 2), ("HTML E CSS", 2),
    ],
    "obrigado": "OBRIGADO POR JOGAR",
}

BG, FG, DIM = "#000000", "#ffffff", "#1a1a1a"
FONT = "'Courier New', Courier, monospace"

# Personagem pixel art (mago). '#' branco, 'o' cinza
SPRITE = [
    "....###....",
    "...#####...",
    "..#######..",
    "...#####...",
    "..#.#.#.#..",
    "..#######..",
    ".#ooooooo#.",
    ".#ooooooo#.",
    "..ooooooo..",
    "..#######..",
    "..##...##..",
    "..##...##..",
]

def sprite(x, y, px=6, extra=""):
    out = [f'<g transform="translate({x},{y})" {extra}>']
    for r, row in enumerate(SPRITE):
        for c, ch in enumerate(row):
            if ch != ".":
                col = FG if ch == "#" else "#9a9a9a"
                out.append(f'<rect x="{c*px}" y="{r*px}" width="{px}" height="{px}" fill="{col}"/>')
    out.append(f'<rect x="{12*px}" y="{2*px}" width="{px}" height="{10*px}" fill="#8a8a8a"/>')
    out.append("</g>")
    return "".join(out)

def esc(t): return html.escape(t)

def banner(c):
    W, H = 880, 280
    stars = "".join(
        f'<rect x="{(i*137)%860+10}" y="{(i*61)%250+10}" width="2" height="2" fill="#fff">'
        f'<animate attributeName="opacity" values="0.1;1;0.1" dur="{2+(i%4)}s" begin="{i*0.3:.1f}s" repeatCount="indefinite"/></rect>'
        for i in range(26)
    )
    bar_w = 410 * c["exp"] / 100
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="{FG}" stroke-width="3"/>
<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="#555" stroke-width="1"/>
{stars}
<text x="440" y="50" fill="#888" font-family="{FONT}" font-size="14" text-anchor="middle" letter-spacing="2">PLAYER 1 · LV 1</text>
<text x="440" y="135" fill="{FG}" font-family="{FONT}" font-size="46" font-weight="bold" text-anchor="middle" letter-spacing="3">{esc(c["nome"])}</text>
<text x="440" y="190" fill="{FG}" font-family="{FONT}" font-size="14" text-anchor="middle" letter-spacing="1">{esc(c["subtitulo"])}</text>
<text x="230" y="237" fill="{FG}" font-family="{FONT}" font-size="12">EXP</text>
<rect x="262" y="226" width="410" height="14" fill="none" stroke="{FG}" stroke-width="1.5"/>
<rect x="262" y="226" width="0" height="14" fill="{FG}"><animate attributeName="width" from="0" to="{bar_w}" dur="2s" fill="freeze"/></rect>
<text x="690" y="237" fill="#888" font-family="{FONT}" font-size="12">{c["exp"]}/100</text>
<text x="85" y="95" fill="#ffe66d" font-family="{FONT}" font-size="11">BUFF! INT +10</text>
<g><animateTransform attributeName="transform" type="translate" values="0,0;0,-5;0,0" dur="1.6s" repeatCount="indefinite"/>
{sprite(70, 120)}</g>
</svg>'''

def atributos(c):
    W, rowh = 880, 38
    H = len(c["atributos"]) * rowh + 40
    rows = []
    for i, (nome, nivel) in enumerate(c["atributos"]):
        y = 28 + i * rowh
        rows.append(f'<text x="40" y="{y+16}" fill="{FG}" font-family="{FONT}" font-size="15">{esc(nome)}</text>')
        for b in range(5):
            on = b < nivel
            rows.append(
                f'<rect x="{290+b*112}" y="{y}" width="106" height="22" fill="{FG if on else DIM}">'
                + (f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{i*0.2+b*0.1:.1f}s" fill="freeze"/>' if on else "")
                + "</rect>"
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="{FG}" stroke-width="3"/>
{"".join(rows)}
</svg>'''

def footer(c):
    W, H = 880, 110
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%">
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="440" y="38" fill="{FG}" font-family="{FONT}" font-size="18" text-anchor="middle" letter-spacing="2">{esc(c["obrigado"])}</text>
<text x="440" y="62" fill="#888" font-family="{FONT}" font-size="12" text-anchor="middle">✔ JOGO SALVO</text>
<rect y="92" width="{W}" height="18" fill="#555"/>
<g><animateTransform attributeName="transform" type="translate" values="-60,0;900,0" dur="14s" repeatCount="indefinite"/>
{sprite(0, 18, 5)}</g>
</svg>'''

if __name__ == "__main__":
    for nome, fn in [("banner", banner), ("atributos", atributos), ("footer", footer)]:
        open(f"assets/{nome}.svg", "w", encoding="utf-8").write(fn(CONFIG))
    print("SVGs gerados em assets/")
