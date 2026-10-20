import os
import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from backend import Backend

def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("VN DELAY")
    engine = QQmlApplicationEngine()
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)
    qml = Path(__file__).resolve().parent / "qml" / "Main.qml"
    engine.load(str(qml))
    if not engine.rootObjects():
        return 1
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
