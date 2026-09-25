"""Gera os SVGs do perfil (banner e barra de linguagens) nos temas claro e escuro."""
from pathlib import Path

AQUI = Path(__file__).parent / "assets"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, Menlo, monospace"

TEMAS = {
    "dark": {
        "bg1": "#0b1220", "bg2": "#111a2e", "borda": "rgba(255,255,255,0.08)",
        "ponto": "#1b2740", "tinta": "#f0f4fa", "tinta2": "#aeb9c9", "mudo": "#7d8aa0",
        "ciano": "#22d3ee", "estrada": "#1d2b44", "faixa": "#3b4d6b",
        "caminhao": "#fbbf24", "cabine": "#fde68a", "vidro": "#0b1220",
        "chip": "rgba(34,211,238,0.10)", "chipborda": "rgba(34,211,238,0.35)",
        # barra de linguagens (paleta validada, passos do escuro)
        "s1": "#3987e5", "s2": "#d95926", "s3": "#199e70", "s4": "#c98500", "outros": "#4a4f5a",
    },
    "light": {
        "bg1": "#f7f9fc", "bg2": "#eef3f9", "borda": "rgba(11,18,32,0.10)",
        "ponto": "#dde5ef", "tinta": "#0f172a", "tinta2": "#475569", "mudo": "#64748b",
        "ciano": "#0891b2", "estrada": "#dbe4ee", "faixa": "#a9b8ca",
        "caminhao": "#d97706", "cabine": "#f59e0b", "vidro": "#fff7e6",
        "chip": "rgba(8,145,178,0.08)", "chipborda": "rgba(8,145,178,0.35)",
        "s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a", "s4": "#eda100", "outros": "#c3c2b7",
    },
}

# Rota: curva suave que passa pelos sistemas. Os nos ficam nos extremos das
# curvas, entao estao exatamente sobre o caminho.
NOS = [
    (640, 214, "Base", "abaixo"),
    (760, 124, "Etapas", "acima"),
    (880, 214, "Motor API", "abaixo"),
    (1000, 124, "Tabela de Frete", "acima"),
    (1120, 214, "Ponto Digital", "abaixo"),
]


def caminho() -> str:
    x0, y0, *_ = NOS[0]
    d = f"M{x0} {y0}"
    for (xa, ya, *_), (xb, yb, *_) in zip(NOS, NOS[1:]):
        meio = (xa + xb) / 2
        d += f" C{meio:.0f} {ya},{meio:.0f} {yb},{xb} {yb}"
    return d


def banner(t: dict) -> str:
    d = caminho()
    nos = []
    for i, (x, y, nome, lado) in enumerate(NOS):
        ly = y + 34 if lado == "abaixo" else y - 22
        atraso = f"{i * 0.6:.1f}s"
        nos.append(f"""
    <circle cx="{x}" cy="{y}" r="9" class="pulso" style="animation-delay:{atraso}"/>
    <circle cx="{x}" cy="{y}" r="8" fill="{t['bg1']}" stroke="{t['ciano']}" stroke-width="3"/>
    <circle cx="{x}" cy="{y}" r="3" fill="{t['ciano']}"/>
    <text x="{x}" y="{ly}" class="no" text-anchor="middle">{nome}</text>""")

    chips = ["23 apps em produção", "1 biblioteca base", "PHP · JS · Python"]
    chips_svg = []
    x = 56
    for texto in chips:
        largura = 16 + len(texto) * 7.6
        chips_svg.append(
            f'<rect x="{x}" y="236" width="{largura:.0f}" height="28" rx="14" fill="{t["chip"]}" stroke="{t["chipborda"]}"/>'
            f'<text x="{x + largura / 2:.0f}" y="255" class="chip" text-anchor="middle">{texto}</text>'
        )
        x += largura + 10

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300" role="img" aria-labelledby="titulo desc">
  <title id="titulo">João Epaminondas</title>
  <desc id="desc">Dev full stack na Rota7 Solutions. Um caminhao percorre uma rota que liga os sistemas Base, Etapas, Motor API, Tabela de Frete e Ponto Digital.</desc>
  <defs>
    <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg1']}"/>
      <stop offset="1" stop-color="{t['bg2']}"/>
    </linearGradient>
    <pattern id="grade" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{t['ponto']}"/>
    </pattern>
    <linearGradient id="esmaece" x1="560" y1="0" x2="820" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="mascara-grade"><rect x="560" width="640" height="300" fill="url(#esmaece)"/></mask>
    <clipPath id="cartao"><rect width="1200" height="300" rx="18"/></clipPath>
    <path id="rota" d="{d}"/>
  </defs>
  <style>
    .nome {{ font: 700 50px {SANS}; fill: {t['tinta']}; letter-spacing: -0.5px; }}
    .cargo {{ font: 500 21px {SANS}; fill: {t['tinta2']}; }}
    .prompt {{ font: 500 15px {MONO}; fill: {t['ciano']}; }}
    .cursor {{ fill: {t['ciano']}; animation: pisca 1.1s steps(1) infinite; }}
    .no {{ font: 600 14px {SANS}; fill: {t['tinta2']}; }}
    .chip {{ font: 600 13px {MONO}; fill: {t['tinta2']}; }}
    .faixa {{ fill: none; stroke: {t['faixa']}; stroke-width: 2; stroke-dasharray: 10 12; animation: anda 1.2s linear infinite; }}
    .pulso {{ fill: none; stroke: {t['ciano']}; stroke-width: 2; opacity: 0; transform-box: fill-box; transform-origin: center; animation: pulso 3s ease-out infinite; }}
    @keyframes anda {{ to {{ stroke-dashoffset: -22; }} }}
    @keyframes pisca {{ 50% {{ opacity: 0; }} }}
    @keyframes pulso {{ 0% {{ opacity: .7; transform: scale(1); }} 70%, 100% {{ opacity: 0; transform: scale(2.6); }} }}
    @media (prefers-reduced-motion: reduce) {{ .faixa, .pulso, .cursor {{ animation: none; }} }}
  </style>

  <g clip-path="url(#cartao)">
    <rect width="1200" height="300" fill="url(#fundo)"/>
    <rect x="560" width="640" height="300" fill="url(#grade)" mask="url(#mascara-grade)"/>

    <!-- estrada -->
    <use href="#rota" fill="none" stroke="{t['estrada']}" stroke-width="16" stroke-linecap="round"/>
    <use href="#rota" class="faixa"/>
    {''.join(nos)}

    <!-- caminhao -->
    <g>
      <g transform="translate(0,-1)">
        <rect x="-26" y="-8" width="28" height="16" rx="2.5" fill="{t['caminhao']}"/>
        <rect x="4" y="-7" width="13" height="14" rx="3.5" fill="{t['cabine']}"/>
        <rect x="11" y="-5" width="4" height="10" rx="1" fill="{t['vidro']}"/>
      </g>
      <animateMotion dur="9s" repeatCount="indefinite" rotate="auto" keyPoints="0;1;1" keyTimes="0;0.85;1" calcMode="linear">
        <mpath href="#rota"/>
      </animateMotion>
    </g>

    <!-- texto -->
    <text x="56" y="78" class="prompt">~/rota7 $ whoami<tspan class="cursor"> ▍</tspan></text>
    <text x="56" y="140" class="nome">João Epaminondas</text>
    <text x="56" y="178" class="cargo">Dev full stack · Rota7 Solutions</text>
    <text x="56" y="208" class="cargo" style="font-size:17px;fill:{t['mudo']}">Sistemas que movem a logística, do banco de dados ao caminhão.</text>
    {''.join(chips_svg)}
  </g>
  <rect x="0.5" y="0.5" width="1199" height="299" rx="17.5" fill="none" stroke="{t['borda']}"/>
</svg>
"""


# Linguagens dos 34 repositorios proprios e da Rota-7, por volume de codigo
# (API /languages do GitHub, 25/09/2026). Outros = TypeScript, Dart, Hack,
# HTML e o resto abaixo de 1%.
LINGUAGENS = [
    ("PHP", 60.6, "s1"),
    ("JavaScript", 22.4, "s2"),
    ("CSS", 7.4, "s3"),
    ("Python", 4.9, "s4"),
    ("Outros", 4.7, "outros"),
]


def linguagens(t: dict) -> str:
    largura, x0, y0, altura, vao = 1200, 0, 44, 18, 2
    util = largura - vao * (len(LINGUAGENS) - 1)
    segmentos, legenda = [], []
    x = x0
    for i, (nome, pct, cor) in enumerate(LINGUAGENS):
        w = util * pct / 100
        primeiro, ultimo = i == 0, i == len(LINGUAGENS) - 1
        # cantos de 4px so nas pontas da barra
        rx = 4
        if primeiro or ultimo:
            segmentos.append(
                f'<rect x="{x:.1f}" y="{y0}" width="{w:.1f}" height="{altura}" rx="{rx}" fill="{t[cor]}"/>'
                + (f'<rect x="{x + w - rx:.1f}" y="{y0}" width="{rx}" height="{altura}" fill="{t[cor]}"/>' if primeiro
                   else f'<rect x="{x:.1f}" y="{y0}" width="{rx}" height="{altura}" fill="{t[cor]}"/>')
            )
        else:
            segmentos.append(f'<rect x="{x:.1f}" y="{y0}" width="{w:.1f}" height="{altura}" fill="{t[cor]}"/>')
        x += w + vao

    lx = 0
    for nome, pct, cor in LINGUAGENS:
        valor = f"{pct:.1f}%".replace(".", ",")
        legenda.append(
            f'<rect x="{lx}" y="90" width="12" height="12" rx="3" fill="{t[cor]}"/>'
            f'<text x="{lx + 20}" y="101" class="leg"><tspan class="leg-nome">{nome}</tspan> {valor}</text>'
        )
        lx += 20 + (len(nome) + 1 + len(valor)) * 7.4 + 30

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" width="1200" height="120" role="img" aria-labelledby="titulo desc">
  <title id="titulo">Linguagens</title>
  <desc id="desc">{'; '.join(f'{n} {p:.1f}%' for n, p, _ in LINGUAGENS)} do codigo em 34 repositorios.</desc>
  <style>
    .tit {{ font: 600 15px {SANS}; fill: {t['tinta']}; }}
    .sub {{ font: 400 13px {SANS}; fill: {t['mudo']}; }}
    .leg {{ font: 400 14px {SANS}; fill: {t['tinta2']}; }}
    .leg-nome {{ font-weight: 600; fill: {t['tinta']}; }}
  </style>
  <text x="0" y="22" class="tit">Linguagens</text>
  <text x="92" y="22" class="sub">por volume de código em 34 repositórios (pessoais + Rota-7)</text>
  {''.join(segmentos)}
  {''.join(legenda)}
</svg>
"""


for nome, t in TEMAS.items():
    (AQUI / f"banner-{nome}.svg").write_text(banner(t), encoding="utf-8")
    (AQUI / f"linguagens-{nome}.svg").write_text(linguagens(t), encoding="utf-8")
print("ok")
