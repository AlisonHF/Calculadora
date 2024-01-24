from typing import TYPE_CHECKING, Callable
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (QLineEdit, QLabel, QWidget, QPushButton,
                                QGridLayout, QMessageBox)
from variables import (BIG_FONT_SIZE, MEDIUM_FONT_SIZE, MINIMUM_WIDTH,
                        TEXTE_MARGIN)
from variables import SMALL_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, converToNumber
import math
from main_window import MainWindow



# Display ( Escrita )
class Display(QLineEdit):
    # Sinal para as teclas
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configStyle()

    # Configuração do estilo da janela
    def configStyle(self) -> None:
        # Set do tamanho da fonte
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px')

        # Set do tamanho da altura
        self.setMinimumHeight(BIG_FONT_SIZE * 2)

        # Set do tamanho da largura
        self.setMinimumWidth(MINIMUM_WIDTH)

        # Set do alinhamento do texto
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Set da margem do texto
        self.setTextMargins(*[TEXTE_MARGIN for c in range(4)])

    # Função que recebe o evento do pressionamento de alguma tecla
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        # Tecla pressionada
        key = event.key()
        # Teclas disponiveis
        KEYS = Qt.Key

        # A operação e a lista de teclas disponiveis para tal
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [
            KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk,
            KEYS.Key_P,
        ] 
        # Se for enter
        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
        
        # Se for delete
        if isDelete:
            self.delPressed.emit()

        # Se for esc
        if isEsc:
            self.clearPressed.emit()
            return event.ignore()
        
        # Se for operador
        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()

        # Se for vazio
        if isEmpty(text):
            return event.ignore()
        
        # Se for um número ou ponto
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()

# Info ( Local da conta )
class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self) -> None:
        # Set do tamanho da fonte
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px')   

        # Set do alinhamento do texto
        self.setAlignment(Qt.AlignmentFlag.AlignRight)    

# Button
class Button(QPushButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self) -> None:
        # Setando a fonte e tamanhos
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

# Grid
class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: MainWindow,
                  *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Lista dos caracteres no grid
        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]

        # Definindo o display
        self.display = display

        # Definindo o info
        self.info = info

        # Definindo a variavel da equação
        self._equation = ''
        self._equationInitialValue = 'Sua conta'

        # Variaveis da conta
        self._left = None
        self._right = None
        self._op = None

        # Set da equation inicial
        self.equation = self._equationInitialValue

        # Window
        self.window = window

        # Sempre é inicializado junto com a class (opcional)
        self._makeGrid()

    # Getter de _equation
    @property
    def equation(self) -> str:
        return self._equation
    
    # Setter de _equation
    @equation.setter
    def equation(self, value: str) -> None:
        self._equation = value
        # Passa o valor para o info
        self.info.setText(value)

    # Constroi o grid com os caracteres
    def _makeGrid(self) -> None:

        # Conecta o sinal das teclas com o display
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        # rowNumber [I das listas ], rowData [a lista ]
        for rowNumber, rowData in enumerate(self._gridMask):
            # colNumber [I dos caracteres ], buttonText [o caractere ]
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                # Checa se é numero, ponto e vazio e aplica a cor caso especial
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    # Configura o botão especial
                    self._configSpecialButton(button)

                # Adiciona o botão no grid
                self.addWidget(button, rowNumber, colNumber)

                # Cria o slot da ação (Para ação)
                buttonSlot = self._makeSlot(
                    self._insertToDisplay, buttonText
                )
                button.clicked.connect(buttonSlot)

    # Função que conecta um botão com um slot
    def _connectButtonClicked(self, button, slot) -> None:
        button.clicked.connect(slot)

    # Função para config dos botões especiais
    def _configSpecialButton(self, button) -> None:
        text = button.text()

        if text == 'C':
            # Limpa o display
            self._connectButtonClicked(button, self._clear)
        
        if text == 'D':
            # Funciona como um backspace
            self._connectButtonClicked(button, self._backspace)

        if text == 'N':
            # Inverte o sinal do número
            self._connectButtonClicked(button, self._invertNumber)

        if text in '+-/*^':
            # Conecta o slot com botão e a função de operator
            self._connectButtonClicked(button, self._makeSlot(
                self._configLeftOp, text
            ))

        if text == '=':
            # Define o botão de igual
            self._connectButtonClicked(button, self._eq)

    # Cria uma função aninhada que executa uma função como Slot:       
    @Slot()
    def _makeSlot(self, func: Callable, *args, **kwargs) -> Callable:
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    # Slot para a função de inverter o sinal do número
    @Slot()
    def _invertNumber(self) -> None:
        displayText = self.display.text()

        # Se não for um número válido ele não insere no display
        if not isValidNumber(displayText):
            return
        
        # Inverte o sinal
        number = converToNumber(displayText) * -1
        self.display.setText(str(number))
        self.display.setFocus()

    # Insere o texto do botão no display
    def _insertToDisplay(self, text: str) -> None:
        # Atualiza o texto do display
        newDisplayValue = self.display.text() + text

        # Se não for um número válido ele não insere no display
        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(text)
        self.display.setFocus()

    # Slot de config do clear do botão 'C'
    @Slot()
    def _clear(self) -> None:
        # Limpa todas as váriaveis
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    # Slot do igual
    @Slot()
    def _eq(self) -> None:
        displayText = self.display.text()

        # Se não for um número:
        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta')
            return
        
        # Adiciona o numero do display no lado direito
        self._right = converToNumber(displayText)
        # Cria a variavel da equação
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        # Verifica a equation
        try:
            # Verifica se a conta é uma potenciacao
            if '^' in self.equation and isinstance(self._left, (float, int)):
                result = math.pow(self._left, self._right)
                result = converToNumber(str(result))
            else:
                result = eval(self.equation)

        # Verifica se é uma divisão por 0
        except ZeroDivisionError:
            self._showError('Divisão por 0')

        # Verifica se o número pode causar um overflow
        except OverflowError:
            self._showError('Essa conta não pode ser realizada')

        self.display.clear()

        # Mostra o resultado no info
        self.info.setText(f'{self.equation} = {result}')

        # Pega o resultado e joga para esquerda
        self._left = result
        self._right = None
        self.display.setFocus()

        # Verifica se houve algum erro na equation e limpa a direita
        if result == 'error':
            self._left = None

    # Slot do backspace
    @Slot()
    def _backspace(self) -> None:
        self.display.backspace()
        self.display.setFocus()

    # Função de botões operadores
    def _configLeftOp(self, text: str) -> None:
        displayText = self.display.text()

        # Limpa o display para digitar o número da direita
        self.display.clear()

        # Se não houver número e algum operador for clicado:
        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada!')
            return
        self.display.setFocus()
        
        # Coloca o primeiro número para a esquerda
        if self._left is None:
            self._left = converToNumber(displayText)

        # Define o op e a equation
        self._op = text
        self.equation = f'{self._left} {self._op}'

    # Telas de avisos
    def _makeDialog(self, text: str) -> QMessageBox:
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox
    
    # Tela de erro
    def _showError(self, text) -> None:
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    # Tela de informação
    def _showInfo(self, text) -> None:
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()
