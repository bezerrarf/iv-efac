import os
from typing import List, Dict

FRASES_PADRAO: List[Dict[str, str]] = [
    {
        "autor": "Albert Einstein",
        "area": "Física Teórica • Prêmio Nobel",
        "icone": "atom",
        "cor": "#00ADB5",
        "frase": "A imaginação é mais importante que o conhecimento. O conhecimento é limitado, enquanto a imaginação abraça o mundo inteiro, estimulando o progresso.",
    },
    {
        "autor": "Marie Curie",
        "area": "Física & Química • 2x Prêmio Nobel",
        "icone": "sparkles",
        "cor": "#f43f5e",
        "frase": "Nada na vida deve ser temido, somente compreendido. Agora é o momento de compreender mais, para que possamos temer menos. Aproveite as descobertas do simpósio!",
    },
    {
        "autor": "Alan Turing",
        "area": "Pioneiro da Ciência da Computação & Matemática",
        "icone": "cpu",
        "cor": "#818cf8",
        "frase": "Às vezes são as pessoas de quem ninguém espera nada que fazem as coisas que ninguém jamais poderia imaginar. Dedique-se e transforme suas ideias em realidade.",
    },
    {
        "autor": "Richard Feynman",
        "area": "Física Quântica • Prêmio Nobel",
        "icone": "zap",
        "cor": "#eab308",
        "frase": "Para aqueles que não conhecem matemática, é difícil sentir a beleza mais profunda da natureza. Se você quer aprender sobre o universo, mergulhe na física e na matemática.",
    },
    {
        "autor": "Ada Lovelace",
        "area": "Pioneira da Computação & Matemática",
        "icone": "code",
        "cor": "#a855f7",
        "frase": "O motor analítico tece padrões algébricos tal como o tear de Jacquard tece flores e folhas. A computação é uma extensão ilimitada da nossa inteligência.",
    },
    {
        "autor": "Carl Sagan",
        "area": "Astrofísica & Divulgação Científica",
        "icone": "telescope",
        "cor": "#38bdf8",
        "frase": "Diante da vastidão do cosmos e da imensidão do tempo, é uma alegria compartilhar um planeta e uma era com mentes tão brilhantes. Aproveite cada minuto do IV EFAC!",
    },
    {
        "autor": "Stephen Hawking",
        "area": "Cosmologia Teórica & Gravitação",
        "icone": "orbit",
        "cor": "#06b6d4",
        "frase": "Lembre-se sempre de olhar para cima, para as estrelas, e não para baixo, para os seus pés. Seja curioso e nunca desista de compreender as leis do universo.",
    },
    {
        "autor": "Katherine Johnson",
        "area": "Matemática Orbital • Trajetórias da NASA",
        "icone": "rocket",
        "cor": "#10b981",
        "frase": "Tudo na natureza é física e matemática aplicada. Apaixone-se pelo que você estuda e dê o seu melhor em cada cálculo e observação.",
    },
]


def carregar_frases_cientistas(caminho_arquivo: str = "frases_cientistas.txt") -> List[Dict[str, str]]:
    """Carrega as frases inspiradoras do arquivo frases_cientistas.txt com fallback gracioso."""
    candidatos = [
        caminho_arquivo,
        os.path.join("assets", "frases_cientistas.txt"),
        os.path.join(os.path.dirname(__file__), "..", "..", "frases_cientistas.txt"),
    ]

    arquivo_valido = None
    for cand in candidatos:
        if os.path.exists(cand):
            arquivo_valido = cand
            break

    if not arquivo_valido:
        return FRASES_PADRAO

    frases_carregadas = []
    try:
        with open(arquivo_valido, "r", encoding="utf-8") as f:
            for line in f:
                linha = line.strip()
                if not linha or linha.startswith("#"):
                    continue
                partes = [p.strip() for p in linha.split("|")]
                if len(partes) >= 5:
                    autor, area, icone, cor, frase = partes[0], partes[1], partes[2], partes[3], partes[4]
                    frases_carregadas.append({
                        "autor": autor,
                        "area": area,
                        "icone": icone or "sparkles",
                        "cor": cor or "#00ADB5",
                        "frase": frase,
                    })
    except Exception:
        return FRASES_PADRAO

    return frases_carregadas if frases_carregadas else FRASES_PADRAO
