# main.py
import sys
from PyQt5.QtWidgets import QApplication
import interface
import importlib
importlib.reload(interface)

def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)

    window = interface.DateSelector()
    window.show()

    if not QApplication.instance().startingUp():
        sys.exit(app.exec_())


# outside QGIS
if __name__ == "__main__":
    main()

# inside QGIS
if __name__ == '__console__':
    date_selector = interface.DateSelector()
    date_selector.show()