# main.py
import sys
from PyQt5.QtWidgets import QApplication
import input

def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)

    window = input.DateSelector()
    window.show()

    if not QApplication.instance().startingUp():
        sys.exit(app.exec_())

# outside QGIS
if __name__ == "__main__":
    main()

# inside QGIS
if __name__ == '__console__':
    date_selector = input.DateSelector()
    date_selector.show()