import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

FREQUENCIA = 16000
DURACAO = 5

print("Carregando modelo de reconhcimento....")
modelo = WhisperModel("small", device="cpu", compute_type="int8")

def ouvir():
    print("\nEstou ouvindo! Fale agora.")
    
    audio = sd.rec(
        int(DURACAO * FREQUENCIA), 
        samplerate=FREQUENCIA,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    
    arquivo = "gravacao.wav"
    write(arquivo, FREQUENCIA, audio)
    
    print("Reconhecendo sua fala...")
    
    segmentos, informacoes = modelo.transcribe(
        arquivo,
        language="pt"
    )
    
    texto = " ".join(
        segmento.text.strip()
        for segmento in segmentos
    )
    
    print(texto if texto else "(nenhuma fala reconhecida)")
    
    return texto.lower().strip()
