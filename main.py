
import subprocess
import webbrowser
import sys
import threading

from pathlib import Path

from PySide6.QtCore import (
    QUrl,
    QThread,
    Signal,
    Slot,
    QObject
)

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from teste_voz import ouvir
from sistema.audio import reproduzir
from interface.app import aplicar_blur_windows
from sistema.interpretador import interpretar_comando
from sistema.aplicativos import abrir_aplicativo

# ==========================================
# COMANDOS DO EPAMIN
# ==========================================

def abrir_plano_aula():
    webbrowser.open(
        "https://docs.google.com/spreadsheets/d/1Gru8fde-cISpkwAxOc_72EwHXjiO_X7LwdiREeOy4To/edit?gid=615737568#gid=615737568"
    )
    print("Abrindo o plano de aula")


def abrir_calculadora():
    subprocess.Popen("calc.exe")
    print("Abrindo a calculadora!")


def abrir_paint():
    subprocess.Popen("mspaint.exe")
    print("Abrindo o Paint!")


def executar_comando(comando):

    intencao = interpretar_comando(comando)

    print(f"Intenção identificada: {intencao}")

    match intencao:

        case "abrir_calculadora":
            abrir_calculadora()
            return "calculadora", True

        case "abrir_paint":
            abrir_paint()
            return "paint", True

        case "abrir_aulas":
            abrir_plano_aula()
            return "aulas", True

        case "sair":
            print("Até logo!")
            return "encerramento", False

        case "abrir_league_of_legends":
            sucesso = abrir_aplicativo("league_of_legends")
            return ("league_of_legends" if sucesso else "nao_entendi"), True

        case "abrir_valorant":
            sucesso = abrir_aplicativo("valorant")
            return ("valorant" if sucesso else "nao_entendi"), True

        case "abrir_rocket_league":
            sucesso = abrir_aplicativo("rocket_league")
            return ("rocket_league" if sucesso else "nao_entendi"), True

        case "abrir_whatsapp":
            sucesso = abrir_aplicativo("whatsapp")
            return ("whatsapp" if sucesso else "nao_entendi"), True

        case "abrir_youtube":
            sucesso = abrir_aplicativo("youtube")
            return ("youtube" if sucesso else "nao_entendi"), True

        case "abrir_steam":
            sucesso = abrir_aplicativo("steam")
            return ("steam" if sucesso else "nao_entendi"), True

        case "abrir_discord":
            sucesso = abrir_aplicativo("discord")
            return ("discord" if sucesso else "nao_entendi"), True

        case "abrir_vscode":
            sucesso = abrir_aplicativo("vscode")
            return ("vscode" if sucesso else "nao_entendi"), True

        case "abrir_spotify":
            sucesso = abrir_aplicativo("spotify")
            return ("spotify" if sucesso else "nao_entendi"), True

        case "abrir_fortnite":
            sucesso = abrir_aplicativo("fortnite")
            return ("fortnite" if sucesso else "nao_entendi"), True

        case "abrir_gta":
            sucesso = abrir_aplicativo("gta_v")
            return ("gta_v" if sucesso else "nao_entendi"), True
        
        case _:
            print("Ainda não consegui interpretar esse comando.")
            return "nao_entendi", True


# ==========================================
# SISTEMA DE REPRODUÇÃO
# ==========================================

class FalaEpamin(QThread):

    def __init__(self, audio):
        super().__init__()
        self.audio = audio

    def run(self):
        reproduzir(self.audio)


# ==========================================
# SISTEMA DE ATIVAÇÃO
# ==========================================

FRASE_ATIVACAO = "epamin"


def reconhecer_ativacao(frase):

    alternativas = [
        "epamin",
        "epaminondas",
        "e para mim",
        "epamine",
        "epámin"
    ]

    return any(
        alternativa in frase
        for alternativa in alternativas
    )


# ==========================================
# SISTEMA DE ESCUTA
# ==========================================

class EscutaEpamin(QThread):

    ativado = Signal()
    comando_recebido = Signal(str)
    erro = Signal(str)

    def __init__(self):
        super().__init__()

        self.executando = True
        self.liberacao = threading.Event()

    def parar(self):
        self.executando = False
        self.liberacao.set()

    def liberar_escuta(self):
        self.liberacao.set()

    def aguardar_liberacao(self):

        while self.executando:

            if self.liberacao.wait(timeout=0.1):
                return True

        return False

    def run(self):

        print(f"Olá! Eu sou o {FRASE_ATIVACAO}.")
        print("Aguardando a frase de ativação...")

        while self.executando:

            try:

                # Aguarda a palavra de ativação
                frase = ouvir()

                if not self.executando:
                    break

                if reconhecer_ativacao(frase):

                    print("Epamin ativado!")

                    # Prepara a sincronização com a saudação
                    self.liberacao.clear()

                    # Solicita a ativação da interface
                    self.ativado.emit()

                    # Captura o comando enquanto a saudação toca
                    print("Capturando comando durante a saudação...")

                    comando = ouvir(tempo_espera=15)

                    if not self.executando:
                        break

                    print(f"Comando capturado: {comando!r}")

                    # Aguarda a saudação terminar
                    if not self.aguardar_liberacao():
                        break

                    if not self.executando:
                        break

                    # Prepara a sincronização da resposta
                    self.liberacao.clear()

                    # Envia o comando para o controlador
                    self.comando_recebido.emit(comando)

                    # Aguarda o processamento e a resposta
                    if not self.aguardar_liberacao():
                        break

                    if not self.executando:
                        break

                    print("Voltando ao modo de espera...")

            except Exception as erro:
                self.erro.emit(str(erro))
                break


# ==========================================
# CONTROLE DA INTERFACE
# ==========================================

class Controlador(QObject):

    def __init__(self, janela, aplicativo, escuta):
        super().__init__()

        self.janela = janela
        self.aplicativo = aplicativo
        self.escuta = escuta

        self.fala_thread = None
        self.proxima_acao = None

        self.ocupado = False

    def definir_estado(self, estado):

        self.janela.setProperty("estadoEpamin", estado)

        print(f"Estado do Epamin: {estado}")

    def iniciar_fala(self, audio, proxima_acao):

        if self.fala_thread is not None and self.fala_thread.isRunning():

            print("Reprodução já em andamento. Solicitação ignorada.")
            return False

        self.proxima_acao = proxima_acao

        self.fala_thread = FalaEpamin(audio)

        self.fala_thread.finished.connect(
            self.finalizar_fala
        )

        self.fala_thread.start()

        return True

    @Slot()
    def ativar(self):

        if self.ocupado:
            print("Epamin já está ocupado.")
            return

        self.ocupado = True

        print("Manifestando interface...")

        self.janela.setProperty("epaminAtivo", True)

        self.definir_estado("ativacao")

        self.iniciar_fala(
            "ativacao",
            "continuar"
        )

    @Slot(str)
    def processar_comando(self, comando):

        if not self.ocupado:
            print("Comando ignorado: nenhuma interação ativa.")
            return

        print(f"Comando recebido: {comando}")

        self.definir_estado("execucao")

        audio, continuar = executar_comando(comando)

        if continuar:
            proxima_acao = "voltar_espera"
        else:
            proxima_acao = "encerrar"

        self.iniciar_fala(audio, proxima_acao)

    @Slot()
    def finalizar_fala(self):

        acao = self.proxima_acao

        self.proxima_acao = None
        self.fala_thread = None

        if acao == "continuar":

            self.definir_estado("escuta")

            # Libera a sincronização da captura
            self.escuta.liberar_escuta()

        elif acao == "voltar_espera":

            print("Reproduzindo aviso de modo de espera...")

            self.definir_estado("escuta")

            self.iniciar_fala(
                "modo_espera",
                "finalizar_espera"
            )

        elif acao == "finalizar_espera":

            print("Epamin retornou ao modo de espera.")

            self.ocupado = False

            self.janela.setProperty("epaminAtivo", False)

            # Retorna ao reconhecimento da ativação
            self.escuta.liberar_escuta()

        elif acao == "encerrar":

            self.ocupado = False

            self.janela.setProperty("epaminAtivo", False)

            self.escuta.parar()

            self.aplicativo.quit()

    @Slot(str)
    def mostrar_erro(self, mensagem):

        print(f"Erro no sistema de escuta: {mensagem}")


# ==========================================
# INICIALIZAÇÃO
# ==========================================

def iniciar_epamin():

    print("EPAMIN: iniciando sistema...")

    aplicativo = QGuiApplication(sys.argv)

    aplicativo.setApplicationName("Epamin")

    engine = QQmlApplicationEngine()

    arquivo_qml = (
        Path(__file__).parent /
        "interface" /
        "main.qml"
    )

    engine.load(QUrl.fromLocalFile(str(arquivo_qml)))

    if not engine.rootObjects():

        print("Erro ao carregar a interface do Epamin.")

        return 1

    janela = engine.rootObjects()[0]

    aplicar_blur_windows(janela)

    escuta = EscutaEpamin()

    controlador = Controlador(
        janela,
        aplicativo,
        escuta
    )

    escuta.ativado.connect(
        controlador.ativar
    )

    escuta.comando_recebido.connect(
        controlador.processar_comando
    )

    escuta.erro.connect(
        controlador.mostrar_erro
    )

    escuta.start()

    print("EPAMIN iniciado.")

    resultado = aplicativo.exec()

    escuta.parar()
    escuta.wait()

    return resultado


if __name__ == "__main__":
    sys.exit(iniciar_epamin())
