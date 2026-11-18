import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from collections import deque
import numpy as np
import string
import time

FREQUENCIA = 16000
BLOCO = 1024

# Configurações da detecção de voz
ESPERA_FALA = 8          # Tempo máximo esperando você começar
SILENCIO_FINAL = 0.7     # Silêncio para encerrar a gravação
DURACAO_MAXIMA = 10      # Limite de duração de cada fala

print("Carregando modelo de reconhecimento...")
modelo = WhisperModel("small", device="cpu", compute_type="int8")


def calcular_volume(audio):
    audio = audio.astype(np.float32)
    return np.sqrt(np.mean(audio ** 2))


def ouvir():
    print("\nAguardando sua voz...")

    blocos_silencio = int(SILENCIO_FINAL * FREQUENCIA / BLOCO)
    blocos_maximos = int(DURACAO_MAXIMA * FREQUENCIA / BLOCO)

    audio_gravado = []
    pre_audio = deque(maxlen=4)

    falando = False
    silencio_atual = 0
    inicio = time.monotonic()

    with sd.InputStream(
        samplerate=FREQUENCIA,
        channels=1,
        dtype="int16",
        blocksize=BLOCO
    ) as stream:

        # Mede o ruído ambiente por aproximadamente meio segundo
        volumes_ambiente = []

        for _ in range(8):
            bloco_audio, _ = stream.read(BLOCO)
            volumes_ambiente.append(calcular_volume(bloco_audio))

        ruido_ambiente = float(np.median(volumes_ambiente))
        limite_voz = max(350, ruido_ambiente * 2.5)

        print("Estou ouvindo! Fale agora.")

        while True:
            bloco_audio, _ = stream.read(BLOCO)
            volume = calcular_volume(bloco_audio)

            if not falando:
                pre_audio.append(bloco_audio)

                if volume > limite_voz:
                    falando = True
                    audio_gravado.extend(list(pre_audio))
                    print("Voz detectada!")

                elif time.monotonic() - inicio >= ESPERA_FALA:
                    print("Nenhuma fala detectada.")
                    return ""

            else:
                audio_gravado.append(bloco_audio)

                if volume > limite_voz:
                    silencio_atual = 0
                else:
                    silencio_atual += 1

                duracao_blocos = len(audio_gravado)

                if silencio_atual >= blocos_silencio:
                    break

                if duracao_blocos >= blocos_maximos:
                    break

    audio = np.concatenate(audio_gravado, axis=0)

    arquivo = "gravacao.wav"
    write(arquivo, FREQUENCIA, audio)

    print("Reconhecendo sua fala...")

    segmentos, informacoes = modelo.transcribe(
        arquivo,
        language="pt",
        initial_prompt="Epamin é o nome de um assistente virtual.",
        beam_size=1,
        vad_filter=True
    )

    texto = " ".join(
        segmento.text.strip()
        for segmento in segmentos
    )

    texto = texto.lower().translate(
        str.maketrans("", "", string.punctuation)
    ).strip()

    print(texto if texto else "(nenhuma fala reconhecida)")

    return texto
