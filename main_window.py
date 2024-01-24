from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
import qdarktheme
from variables import PRIMARY_COLOR, DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR



# Janela principal
class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Configurando o Layout
        self.cw = QWidget()
        
        # Tipo do layout
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)

        # Titulo da janela
        self.setWindowTitle('Calculadora')

    # Função para adicionar widgets para o layout
    def addWidgetToVLayout(self, widget: QWidget) -> None:
        self.vLayout.addWidget(widget)

    # Função para determinar o tamanho da janela
    def adjustFixedSize(self) -> None:
        # Ultima coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    # Construtor de janelas
    def makeMsgBox(self) -> QMessageBox:
        return QMessageBox(self)

    

# Setando o tema
# Criando configs para as cores mudarem quando o mouse passar pelo botão
# e pressionar o botão
qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""

# Set do tema
def setupTheme() -> None:
    qdarktheme.setup_theme(
        theme='dark',
        corner_shape='rounded',
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=qss
    )
