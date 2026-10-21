import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

FREQUENCIA = 16000
DURACAO = 5

print("Carregando modelo de reconhcimento....")
modelo = WhisperModel("base", device="cpu", compute_type="int8")

input("Pressione ENTER e prepare-se para falar....")

print("Estou ouvindo! Fale agora.")

audio = sd.rec(
    int(DURACAO * FREQUENCIA),
    samplerate=FREQUENCIA,
    channels=1,
    dtype="int16"
)

sd.wait()

write("gravacao.wav", FREQUENCIA, audio)
print("Áudio gravado! Reconhecendo sua fala...")

segmentos, informacoes = modelo.transcribe(
    "gravacao.wav",
    language="pt"
)

texto= " ".join(segmento.text.strip() for segmento in segmentos)

print("\nVocê disse:", texto if texto else "(nenhuma fala reconhecida)")