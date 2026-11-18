
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from collections import deque
import numpy as np
import string
import time
import tempfile
import os


# ==========================================
# CONFIGURAÇÕES
# ==========================================

FREQUENCIA = 16000
BLOCO = 1024

ESPERA_FALA = 8
SILENCIO_FINAL = 0.7
DURACAO_MAXIMA = 10


# ==========================================
# CARREGAMENTO DO MODELO
# ==========================================

print("Carregando modelo de reconhecimento...")

modelo = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


# ==========================================
# DETECÇÃO DE VOLUME
# ==========================================

def calcular_volume(audio):

    audio = audio.astype(np.float32)

    return np.sqrt(np.mean(audio ** 2))


# ==========================================
# RECONHECIMENTO DE VOZ
# ==========================================

def ouvir(tempo_espera=ESPERA_FALA):

    print("\nAguardando sua voz...")

    blocos_silencio = int(
        SILENCIO_FINAL * FREQUENCIA / BLOCO
    )

    blocos_maximos = int(
        DURACAO_MAXIMA * FREQUENCIA / BLOCO
    )

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

        # Analisa o ruído ambiente
        volumes_ambiente = []

        for _ in range(8):

            bloco_audio, _ = stream.read(BLOCO)

            volumes_ambiente.append(
                calcular_volume(bloco_audio)
            )

        ruido_ambiente = float(
            np.median(volumes_ambiente)
        )

        limite_voz = max(
            350,
            ruido_ambiente * 2.5
        )

        print("Estou ouvindo! Fale agora.")

        while True:

            bloco_audio, _ = stream.read(BLOCO)

            volume = calcular_volume(bloco_audio)

            if not falando:

                pre_audio.append(bloco_audio)

                if volume > limite_voz:

                    falando = True

                    audio_gravado.extend(
                        list(pre_audio)
                    )

                    print("Voz detectada!")

                elif time.monotonic() - inicio >= tempo_espera:

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

    # ==========================================
    # PREPARAÇÃO DO ÁUDIO
    # ==========================================

    if not audio_gravado:

        return ""

    audio = np.concatenate(
        audio_gravado,
        axis=0
    )

    arquivo_temporario = None

    try:

        # Cria um WAV exclusivo para esta captura
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as arquivo:

            arquivo_temporario = arquivo.name

        write(
            arquivo_temporario,
            FREQUENCIA,
            audio
        )

        # ==========================================
        # TRANSCRIÇÃO
        # ==========================================

        print("Reconhecendo sua fala...")

        segmentos, informacoes = modelo.transcribe(
            arquivo_temporario,
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

        print(
            texto if texto else "(nenhuma fala reconhecida)"
        )

        return texto

    finally:

        # Remove o arquivo temporário
        if arquivo_temporario and os.path.exists(arquivo_temporario):

            os.remove(arquivo_temporario)
