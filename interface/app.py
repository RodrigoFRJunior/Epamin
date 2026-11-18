
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


def iniciar_epamin():
    app = QGuiApplication(sys.argv)

    app.setApplicationName("Epamin")

    engine = QQmlApplicationEngine()

    arquivo_qml = Path(__file__).parent / "main.qml"

    engine.load(QUrl.fromLocalFile(str(arquivo_qml)))

    if not engine.rootObjects():
        print("Erro ao carregar a interface do Epamin.")
        return 1

    print("EPAMIN iniciado.")

    return app.exec()


if __name__ == "__main__":
    sys.exit(iniciar_epamin())
