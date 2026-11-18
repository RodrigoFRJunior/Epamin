
import asyncio
import tempfile
import os

import edge_tts
from playsound3 import playsound


VOZ = "pt-BR-AntonioNeural"


async def gerar_audio(texto, arquivo):
    comunicacao = edge_tts.Communicate(
        texto,
        VOZ
    )

    await comunicacao.save(arquivo)


def falar(texto):
    arquivo = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False
        ) as temporario:
            arquivo = temporario.name

        asyncio.run(gerar_audio(texto, arquivo))

        playsound(arquivo, block=True)

    except Exception as erro:
        print(f"Erro na síntese de voz: {erro}")

    finally:
        if arquivo and os.path.exists(arquivo):
            try:
                os.remove(arquivo)
            except OSError:
                pass
