import ast
import operator
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QListWidget
)


# ============================================================
# EVALUADOR DE OPERACIONES
# ============================================================

class Evaluador:
    operaciones = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    @classmethod
    def calcular(cls, texto):

        # Completar paréntesis que falten
        cantidad_abiertos = texto.count("(")
        cantidad_cerrados = texto.count(")")

        if cantidad_abiertos > cantidad_cerrados:
            texto += ")" * (cantidad_abiertos - cantidad_cerrados)

        try:
            arbol = ast.parse(texto, mode="eval")
            return cls._resolver(arbol.body)

        except ZeroDivisionError:
            raise ZeroDivisionError

        except Exception:
            raise ValueError("Expresión incorrecta")

    @classmethod
    def _resolver(cls, nodo):

        # Número
        if isinstance(nodo, ast.Constant):

            if isinstance(nodo.value, (int, float)):
                return nodo.value

            raise ValueError("Número no válido")

        # Operación matemática
        if isinstance(nodo, ast.BinOp):

            izquierda = cls._resolver(nodo.left)
            derecha = cls._resolver(nodo.right)

            operador = type(nodo.op)

            if operador in cls.operaciones:
                return cls.operaciones[operador](
                    izquierda,
                    derecha
                )

        # Número negativo o positivo
        if isinstance(nodo, ast.UnaryOp):

            numero = cls._resolver(nodo.operand)
            operador = type(nodo.op)

            if operador in cls.operaciones:
                return cls.operaciones[operador](numero)

        raise ValueError("Operación no permitida")


# ============================================================
# CALCULADORA
# ============================================================

class Calculadora(QWidget):

    MAX_HISTORIAL = 5

    def __init__(self):
        super().__init__()

        self.expresion = ""
        self.nuevo_numero = False

        self.crear_ventana()
        self.crear_interfaz()
        self.aplicar_diseño()

    # --------------------------------------------------------
    # VENTANA
    # --------------------------------------------------------

    def crear_ventana(self):

        self.setWindowTitle("Mi Calculadora")
        self.setFixedSize(380, 560)

    # --------------------------------------------------------
    # INTERFAZ
    # --------------------------------------------------------

    def crear_interfaz(self):

        principal = QVBoxLayout()

        principal.setContentsMargins(18, 18, 18, 18)
        principal.setSpacing(12)

        # Título
        titulo = QLabel("CALCULADORA")
        titulo.setAlignment(Qt.AlignCenter)

        principal.addWidget(titulo)

        # Pantalla
        self.pantalla = QLineEdit()

        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setPlaceholderText("0")

        principal.addWidget(self.pantalla)

        # ----------------------------------------------------
        # BOTONES
        # ----------------------------------------------------

        teclado = QGridLayout()
        teclado.setSpacing(10)

        botones = [

            ("AC", 0, 0),
            ("(", 0, 1),
            (")", 0, 2),
            ("÷", 0, 3),

            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("x", 1, 3),

            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("-", 2, 3),

            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("+", 3, 3),

            ("0", 4, 0),
            (".", 4, 1),
            ("=", 4, 2)
        ]

        for texto, fila, columna in botones:

            boton = QPushButton(texto)

            boton.setMinimumHeight(55)

            # Tipo de botón
            if texto in ["÷", "×", "-", "+"]:
                boton.setProperty("tipo", "operador")

            elif texto == "=":
                boton.setProperty("tipo", "igual")

            elif texto == "AC":
                boton.setProperty("tipo", "limpiar")

            elif texto in ["(", ")"]:
                boton.setProperty("tipo", "parentesis")

            else:
                boton.setProperty("tipo", "numero")

            boton.clicked.connect(
                lambda _, valor=texto:
                self.procesar(valor)
            )

            # El botón igual ocupa dos espacios
            if texto == "=":
                teclado.addWidget(
                    boton,
                    fila,
                    columna,
                    1,
                    2
                )
            else:
                teclado.addWidget(
                    boton,
                    fila,
                    columna
                )

        principal.addLayout(teclado)

        # ----------------------------------------------------
        # HISTORIAL
        # ----------------------------------------------------

        texto_historial = QLabel("Historial")

        principal.addWidget(texto_historial)

        self.historial = QListWidget()

        self.historial.setFocusPolicy(Qt.NoFocus)

        principal.addWidget(self.historial)

        self.setLayout(principal)

    # --------------------------------------------------------
    # DISEÑO
    # --------------------------------------------------------

    def aplicar_diseño(self):

        estilo = """

        QWidget {
            background-color: #202124;
            color: white;
            font-family: Segoe UI;
        }

        QLabel {
            color: #9aa0a6;
            font-size: 14px;
            font-weight: bold;
        }

        QLineEdit {
            background-color: #303134;
            border: 2px solid #5f6368;
            border-radius: 12px;
            color: white;
            font-size: 30px;
            padding: 12px;
        }

        QListWidget {
            background-color: #303134;
            border: 1px solid #5f6368;
            border-radius: 10px;
            color: #e8eaed;
            padding: 5px;
            font-size: 13px;
        }

        QPushButton {
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
        }

        QPushButton[tipo="numero"] {
            background-color: #3c4043;
            color: white;
        }

        QPushButton[tipo="numero"]:hover {
            background-color: #4a4d51;
        }

        QPushButton[tipo="operador"] {
            background-color: #8ab4f8;
            color: #202124;
        }

        QPushButton[tipo="operador"]:hover {
            background-color: #aecbfa;
        }

        QPushButton[tipo="igual"] {
            background-color: #34a853;
            color: white;
        }

        QPushButton[tipo="igual"]:hover {
            background-color: #5bb974;
        }

        QPushButton[tipo="limpiar"] {
            background-color: #ea4335;
            color: white;
        }

        QPushButton[tipo="limpiar"]:hover {
            background-color: #f06a61;
        }

        QPushButton[tipo="parentesis"] {
            background-color: #5f6368;
            color: white;
        }

        QPushButton[tipo="parentesis"]:hover {
            background-color: #777a7e;
        }

        QPushButton:pressed {
            background-color: #777777;
        }

        """

        self.setStyleSheet(estilo)

    # --------------------------------------------------------
    # PROCESAR BOTONES
    # --------------------------------------------------------

    def procesar(self, valor):

        # Limpiar
        if valor == "AC":

            self.expresion = ""
            self.pantalla.clear()
            self.nuevo_numero = False

            return

        # Igual
        if valor == "=":

            self.calcular_resultado()

            return

        # Después de obtener un resultado,
        # si se pulsa un número empieza una operación nueva
        if self.nuevo_numero and valor in "0123456789.":

            self.expresion = ""

        self.nuevo_numero = False

        self.expresion += valor

        self.pantalla.setText(self.expresion)

    # --------------------------------------------------------
    # CALCULAR
    # --------------------------------------------------------

    def calcular_resultado(self):

        if not self.expresion:
            return

        expresion = self.expresion

        # Cambiar símbolos de la interfaz
        expresion = expresion.replace("÷", "/")
        expresion = expresion.replace("×", "*")

        try:

            resultado = Evaluador.calcular(expresion)

            # Evitar mostrar 5.0 cuando realmente es 5
            if isinstance(resultado, float):

                if resultado.is_integer():
                    resultado = int(resultado)

            resultado_texto = str(resultado)

            # Guardar historial
            registro = (
                f"{self.expresion} = "
                f"{resultado_texto}"
            )

            self.historial.addItem(registro)

            # Máximo 5 operaciones
            while self.historial.count() > self.MAX_HISTORIAL:
                self.historial.takeItem(0)

            self.historial.scrollToBottom()

            # Mostrar resultado
            self.pantalla.setText(resultado_texto)

            self.expresion = resultado_texto

            self.nuevo_numero = True

        except ZeroDivisionError:

            self.pantalla.setText(
                "No se puede dividir entre 0"
            )

            self.expresion = ""
            self.nuevo_numero = False

        except Exception:

            self.pantalla.setText(
                "Error de sintaxis"
            )

            self.expresion = ""
            self.nuevo_numero = False

    # --------------------------------------------------------
    # TECLADO
    # --------------------------------------------------------

    def keyPressEvent(self, event):

        tecla = event.key()
        texto = event.text()

        # Enter
        if tecla in (
            Qt.Key_Return,
            Qt.Key_Enter
        ):

            self.procesar("=")

        # Escape
        elif tecla == Qt.Key_Escape:

            self.procesar("AC")

        # Backspace
        elif tecla == Qt.Key_Backspace:

            self.procesar("AC")

        # Números y operaciones
        elif texto in "0123456789+-./*()":

            conversion = {
                "*": "×",
                "/": "÷"
            }

            valor = conversion.get(
                texto,
                texto
            )

            self.procesar(valor)

        else:

            super().keyPressEvent(event)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    app = QApplication(sys.argv)

    ventana = Calculadora()

    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()