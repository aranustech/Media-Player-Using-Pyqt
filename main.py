import sys
from PyQt6.QtWidgets import QApplication
from contoller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Controller()
    ui.show()
    sys.exit(app.exec())
