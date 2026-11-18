
import re
import unicodedata
from difflib import SequenceMatcher


# ==========================================
# PALAVRAS IGNORADAS
# ==========================================

PALAVRAS_IGNORADAS = {
    "abrir", "abre", "abra",
    "quero", "gostaria",
    "por", "favor", "para", "mim",
    "a", "o", "as", "os",
    "um", "uma", "meu", "minha",
    "meus", "minhas",
    "acessar", "iniciar", "inicia",
    "inicie", "executar", "executa",
    "poderia", "pode",
    "colocar", "coloca", "coloque",
    "iniciar", "inicie",
    "jogar", "jogar", "rodar",
    "entrar", "no", "na", "nos", "nas",
    "aplicativo", "programa", "jogo"
}


# ==========================================
# INTENÇÕES
# ==========================================

INTENCOES = {

    "abrir_calculadora": [
        ("calculadora",),
        ("conta",),
        ("calcular",)
    ],

    "abrir_paint": [
        ("paint",),
        ("mspaint",),
        ("desenhar",)
    ],

    "abrir_aulas": [
        ("aulas",),
        ("aula",),
        ("plano", "aula")
    ],

    "abrir_league_of_legends": [
        ("league", "of", "legends"),
        ("league",),
        ("lol",),
        ("legends",)
    ],

    "abrir_valorant": [
        ("valorant",),
        ("valoran",)
    ],

    "abrir_rocket_league": [
        ("rocket", "league"),
        ("rocket",),
        ("foguete",)
    ],

    "abrir_whatsapp": [
        ("whatsapp",),
        ("what", "sapp")
    ],

    "abrir_youtube": [
        ("youtube",),
        ("you", "tube")
    ],

    "abrir_steam": [
        ("steam",),
        ("sti",)
    ],

    "abrir_discord": [
        ("discord",),
        ("discor",)
    ],

    "abrir_vscode": [
        ("vscode",),
        ("visual", "studio", "code"),
        ("code",)
    ],

    "abrir_spotify": [
        ("spotify",),
        ("spotfy",)
    ],

    "abrir_fortnite": [
        ("fortnite",),
        ("fort", "nite")
    ],

    "abrir_gta": [
        ("gta",),
        ("grand", "theft", "auto"),
        ("grand", "theft"),
        ("gta", "cinco")
    ],

    "sair": [
        ("sair",),
        ("tchau",),
        ("encerrar",),
        ("finalizar",),
        ("ate", "logo")
    ]
}


# ==========================================
# NORMALIZAÇÃO
# ==========================================

def normalizar(texto):

    texto = texto.lower()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    texto = re.sub(
        r"[^a-z0-9\s]",
        " ",
        texto
    )

    palavras = texto.split()

    palavras = [
        palavra
        for palavra in palavras
        if palavra not in PALAVRAS_IGNORADAS
    ]

    return palavras


# ==========================================
# SIMILARIDADE
# ==========================================

def similaridade(palavra1, palavra2):

    return SequenceMatcher(
        None,
        palavra1,
        palavra2
    ).ratio()


def comparar_intencao(palavras_usuario, referencia):

    pontuacoes = []

    for palavra_referencia in referencia:

        melhor_pontuacao = 0

        for palavra_usuario in palavras_usuario:

            pontuacao = similaridade(
                palavra_referencia,
                palavra_usuario
            )

            limite = (
                0.78
                if len(palavra_referencia) >= 5
                else 0.85
            )

            if pontuacao >= limite:

                melhor_pontuacao = max(
                    melhor_pontuacao,
                    pontuacao
                )

        if melhor_pontuacao == 0:
            return 0

        pontuacoes.append(
            melhor_pontuacao
        )

    return sum(pontuacoes) / len(pontuacoes)


# ==========================================
# INTERPRETADOR
# ==========================================

def interpretar_comando(texto):

    palavras_usuario = normalizar(texto)

    if not palavras_usuario:
        return None

    resultados = []

    for intencao, referencias in INTENCOES.items():

        melhor_pontuacao = 0

        for referencia in referencias:

            pontuacao = comparar_intencao(
                palavras_usuario,
                referencia
            )

            melhor_pontuacao = max(
                melhor_pontuacao,
                pontuacao
            )

        if melhor_pontuacao > 0:

            resultados.append(
                (intencao, melhor_pontuacao)
            )

    if not resultados:
        return None

    resultados.sort(
        key=lambda resultado: resultado[1],
        reverse=True
    )

    if (
        len(resultados) > 1
        and resultados[0][1] - resultados[1][1] < 0.08
    ):
        return None

    return resultados[0][0]
