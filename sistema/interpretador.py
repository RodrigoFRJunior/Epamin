
import re
import unicodedata
from difflib import SequenceMatcher


# Palavras que não alteram a intenção principal
PALAVRAS_IGNORADAS = {
    "abrir", "abre", "abra",
    "quero", "gostaria",
    "por", "favor", "para", "mim",
    "a", "o", "as", "os",
    "um", "uma", "meu", "minha",
    "meus", "minhas",
    "acessar", "iniciar", "inicia",
    "inicie", "executar", "executa",
    "poderia", "pode"
}


# Intenções e suas palavras de referência
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

    "sair": [
        ("sair",),
        ("tchau",),
        ("encerrar",),
        ("finalizar",),
        ("ate", "logo")
    ]
}


def normalizar(texto):
    texto = texto.lower()

    # Remove acentos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    # Remove pontuação
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)

    palavras = texto.split()

    # Remove palavras auxiliares
    palavras = [
        palavra
        for palavra in palavras
        if palavra not in PALAVRAS_IGNORADAS
    ]

    return palavras


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

            limite = 0.78 if len(palavra_referencia) >= 5 else 0.85

            if pontuacao >= limite:
                melhor_pontuacao = max(
                    melhor_pontuacao,
                    pontuacao
                )

        if melhor_pontuacao == 0:
            return 0

        pontuacoes.append(melhor_pontuacao)

    return sum(pontuacoes) / len(pontuacoes)


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

    # Evita escolher uma intenção quando duas são
    # praticamente igualmente prováveis.
    if (
        len(resultados) > 1
        and resultados[0][1] - resultados[1][1] < 0.08
    ):
        return None

    return resultados[0][0]
