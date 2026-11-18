
import subprocess
import webbrowser
import sys

from pathlib import Path

from PySide6.QtCore import QUrl, QThread, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject

from teste_voz import ouvir
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

        case "abrir jorge" | "jorge":
            abrir_paint()

        case "aulas":
            abrir_plano_aula()

        case "sair" | "tchau":
            print("Até logo!")
            return False

        case "":
            print("Não consegui entender o comando.")

        case _:
            print("Ainda não conheço esse comando.")

    return True


# ==========================================
# SISTEMA DE ESCUTA
# ==========================================

FRASE_ATIVACAO = "epamin"


class EscutaEpamin(QThread):

    ativado = Signal()
    comando_recebido = Signal(str)
    erro = Signal(str)

    def __init__(self):
        super().__init__()
        self.executando = True

    def parar(self):
        self.executando = False

    def run(self):

        print(f"Olá! Eu sou o {FRASE_ATIVACAO}.")
        print("Aguardando a frase de ativação...")

        while self.executando:

            try:
                frase = ouvir()

                if not self.executando:
                    break

                if FRASE_ATIVACAO in frase:

                    print("Epamin ativado!")

                    self.ativado.emit()

                    print("Diga seu comando.")

                    comando = ouvir()

                    if not self.executando:
                        break

                    self.comando_recebido.emit(comando)

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

    @Slot()
    def ativar(self):
        print("Manifestando interface...")
        self.janela.setProperty("epaminAtivo", True)

    @Slot(str)
    def processar_comando(self, comando):

        print(f"Comando recebido: {comando}")

        continuar = executar_comando(comando)

        # Esconde a interface depois de processar
        self.janela.setProperty("epaminAtivo", False)

        if not continuar:
            self.escuta.parar()
            self.aplicativo.quit()

    @Slot(str)
    def mostrar_erro(self, mensagem):
        print(f"Erro no sistema de escuta: {mensagem}")


# ==========================================
# INICIALIZAÇÃO
# ==========================================

def iniciar_epamin():

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
    escuta.erro.connect(controlador.mostrar_erro)

    escuta.start()

    print("EPAMIN iniciado.")

    resultado = aplicativo.exec()

    escuta.parar()
    escuta.wait()

    return resultado


if __name__ == "__main__":
    sys.exit(iniciar_epamin())
