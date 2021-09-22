import sys
from PyQt5.QtWidgets import QApplication
from InterfaceFunctionality import InterfaceWindow

app = QApplication(sys.argv)
app.setStyle('Fusion')
interface = InterfaceWindow()
sys.exit(app.exec())


