
import sys
import ctypes
from ctypes import wintypes
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


def aplicar_blur_windows(janela):
    """
    Tenta aplicar o blur nativo do Windows atrás da janela.
    Se não estiver disponível, a interface continua funcionando
    com o fundo escuro translúcido definido no QML.
    """

    if sys.platform != "win32":
        return

    try:
        class AccentPolicy(ctypes.Structure):
            _fields_ = [
                ("AccentState", ctypes.c_int),
                ("AccentFlags", ctypes.c_int),
                ("GradientColor", ctypes.c_uint),
                ("AnimationId", ctypes.c_int),
            ]

        class WindowCompositionAttributeData(ctypes.Structure):
            _fields_ = [
                ("Attribute", ctypes.c_int),
                ("Data", ctypes.POINTER(AccentPolicy)),
                ("SizeOfData", ctypes.c_size_t),
            ]

        hwnd = wintypes.HWND(int(janela.winId()))

        # ACCENT_ENABLE_BLURBEHIND
        politica = AccentPolicy()
        politica.AccentState = 3
        politica.AccentFlags = 2
        politica.GradientColor = 0x99030A16
        politica.AnimationId = 0

        dados = WindowCompositionAttributeData()
        dados.Attribute = 19
        dados.Data = ctypes.pointer(politica)
        dados.SizeOfData = ctypes.sizeof(politica)

        user32 = ctypes.windll.user32

        funcao = user32.SetWindowCompositionAttribute
        funcao.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(WindowCompositionAttributeData)
        ]
        funcao.restype = wintypes.BOOL

        resultado = funcao(hwnd, ctypes.byref(dados))

        if resultado:
            print("Blur do Windows aplicado.")
        else:
            print("Blur nativo indisponível. Usando fundo translúcido.")

    except Exception as erro:
        print(f"Não foi possível aplicar o blur: {erro}")


def iniciar_epamin():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Epamin")

    engine = QQmlApplicationEngine()

    arquivo_qml = Path(__file__).parent / "main.qml"

    engine.load(QUrl.fromLocalFile(str(arquivo_qml)))

    if not engine.rootObjects():
        print("Erro ao carregar a interface do Epamin.")
        return 1

    janela = engine.rootObjects()[0]

    aplicar_blur_windows(janela)

    print("EPAMIN iniciado.")

    return app.exec()


if __name__ == "__main__":
    sys.exit(iniciar_epamin())
