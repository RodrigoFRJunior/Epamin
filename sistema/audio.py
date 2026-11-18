
from pathlib import Path
from playsound3 import playsound


PASTA_AUDIO = Path(__file__).parent.parent / "audio"

AUDIOS = {
    "ativacao": "ativacao.mp3",
    "calculadora": "calculadora.mp3",
    "paint": "paint.mp3",
    "aulas": "aulas.mp3",
    "nao_entendi": "nao_entendi.mp3",
    "encerramento": "encerramento.mp3",
}


def reproduzir(nome):
    arquivo_nome = AUDIOS.get(nome)

    if arquivo_nome is None:
        print(f"Áudio não cadastrado: {nome}")
        return False

    arquivo = PASTA_AUDIO / arquivo_nome

    if not arquivo.is_file():
        print(f"Arquivo de áudio não encontrado: {arquivo}")
        return False

    try:
        playsound(str(arquivo), block=True)
        return True

    except Exception as erro:
        print(f"Erro ao reproduzir áudio: {erro}")
        return False
