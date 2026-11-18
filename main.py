
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

    match comando:
        case "abrir calculadora" | "calculadora":
            abrir_calculadora()
            return "calculadora", True

        case "abrir jorge" | "jorge":
            abrir_paint()
            return "paint", True

        case "aulas":
            abrir_plano_aula()
            return "aulas", True

        case "sair" | "tchau":
            print("Até logo!")
            return "encerramento", False

        case "":
            print("Não consegui entender o comando.")
            return "nao_entendi", True

        case _:
            print("Ainda não conheço esse comando.")
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
# SISTEMA DE ESCUTA
# ==========================================

FRASE_ATIVACAO = "epamin"


def reconhecer_ativacao(frase):

    alternativas = [
        "epamin",
        "e para mim",
        "epamine",
        "epámin"
    ]

    return any(
        alternativa in frase
        for alternativa in alternativas
    )


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
                frase = ouvir()

                if not self.executando:
                    break

                if reconhecer_ativacao(frase):

                    print("Epamin ativado!")

                    self.liberacao.clear()
                    self.ativado.emit()

                    if not self.aguardar_liberacao():
                        break

                    if not self.executando:
                        break

                    print("Diga seu comando.")

                    comando = ouvir()

                    if not self.executando:
                        break

                    self.liberacao.clear()
                    self.comando_recebido.emit(comando)

                    if not self.aguardar_liberacao():
                        break

                    if not self.executando:
                        break

                    if comando in ("sair", "tchau"):
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

        # Impede ativações e respostas duplicadas
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

    print("TESTE: NOVO MAIN.PY CARREGADO")

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

    escuta.ativado.connect(controlador.ativar)

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
