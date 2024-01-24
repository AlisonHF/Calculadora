import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow, setupTheme
from variables import WINDOW_ICON_PATH 
from PySide6.QtGui import QIcon
from objects import Display, Info, ButtonsGrid


# Configurando o set do icon
def set_icon(caminho):
     icon = QIcon(str(caminho))
 
     icon.addFile('files/10298172.jpg')
    
     window.setWindowIcon(icon)
    
     app.setWindowIcon(icon)
    
     if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                u'CompanyName.ProductName.SubProduct.VersionInformation')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Setando o tema
    setupTheme()
    window = MainWindow()

    # Info
    info = Info('2.0 ^ 10.0 = 1024')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)


    # Setando icone
    icon = set_icon(WINDOW_ICON_PATH)

    window.show()
    app.exec()
