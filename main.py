import sys

from PyQt5.QtWidgets import QApplication

sys.path.append(r'design')
from creating_interface import Program


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.exit(app.exec())
