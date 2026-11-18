
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
    "modo_espera": "modo_espera.mp3",
    "league_of_legends": "league_of_legends.mp3",
    "valorant": "valorant.mp3",
    "rocket_league": "rocket_league.mp3",
    "whatsapp": "whatsapp.mp3",
    "youtube": "youtube.mp3",
    "steam": "steam.mp3",
    "discord": "discord.mp3",
    "vscode": "vscode.mp3",
    "spotify": "spotify.mp3",
    "fortnite": "fortnite.mp3",
    "gta_v": "gta_v.mp3",
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
