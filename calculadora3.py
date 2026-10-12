
import ast
import operator
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget
)


# =========================================================
# MOTOR DE CALCULO
# =========================================================

class MotorCalculo:

    funciones = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg
    }

    @classmethod
    def ejecutar(cls, expresion):

        cantidad_abierta = expresion.count("(")
        cantidad_cerrada = expresion.count(")")

        if cantidad_abierta > cantidad_cerrada:
            expresion += ")" * (
                cantidad_abierta - cantidad_cerrada
            )

        try:
            arbol = ast.parse(
                expresion,
                mode="eval"
            )

            return cls.resolver(arbol.body)

        except ZeroDivisionError:
            raise ZeroDivisionError

        except Exception:
            raise ValueError("Expresión inválida")

    @classmethod
    def resolver(cls, nodo):

        if isinstance(nodo, ast.Constant):

            if isinstance(nodo.value, (int, float)):
                return nodo.value

            raise ValueError("Valor inválido")

        if isinstance(nodo, ast.BinOp):

            izquierdo = cls.resolver(nodo.left)
            derecho = cls.resolver(nodo.right)

            operacion = type(nodo.op)

            if operacion in cls.funciones:
                return cls.funciones[operacion](
                    izquierdo,
                    derecho
                )

        if isinstance(nodo, ast.UnaryOp):

            valor = cls.resolver(nodo.operand)
            operacion = type(nodo.op)

            if operacion in cls.funciones:
                return cls.funciones[operacion](valor)

        raise ValueError("Operación no permitida")


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

class Calculadora(QMainWindow):

    MAX_OPERACIONES = 5

    def __init__(self):

        super().__init__()

        self.expresion = ""
        self.nuevo_calculo = False

        self.preparar_ventana()
        self.crear_componentes()
        self.dar_estilo()

    # =====================================================
    # CONFIGURACION
    # =====================================================

    def preparar_ventana(self):

        self.setWindowTitle(
            "Calculadora Matemática"
        )

        self.setFixedSize(
            390,
            610
        )

    # =====================================================
    # INTERFAZ
    # =====================================================

    def crear_componentes(self):

        central = QWidget()
        self.setCentralWidget(central)

        principal = QVBoxLayout(central)

        principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        principal.setSpacing(10)

        # Titulo
        titulo = QLabel(
            "CALCULADORA"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setProperty(
            "tipo",
            "titulo"
        )

        principal.addWidget(titulo)

        # Pantalla
        self.display = QLineEdit()

        self.display.setReadOnly(True)

        self.display.setAlignment(
            Qt.AlignRight
        )

        self.display.setPlaceholderText(
            "0"
        )

        principal.addWidget(
            self.display
        )

        # Teclado
        teclado = QGridLayout()

        teclado.setSpacing(7)

        botones = [
            ("C", 0, 0),
            ("(", 0, 1),
            (")", 0, 2),
            ("÷", 0, 3),

            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("×", 1, 3),

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

        for nombre, fila, columna in botones:

            boton = QPushButton(nombre)

            boton.setMinimumHeight(48)

            boton.setProperty(
                "categoria",
                self.tipo_boton(nombre)
            )

            boton.clicked.connect(
                lambda _, x=nombre:
                self.recibir(x)
            )

            if nombre == "=":

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

        # Historial
        texto_historial = QLabel(
            "Historial de operaciones"
        )

        texto_historial.setProperty(
            "tipo",
            "subtitulo"
        )

        principal.addWidget(
            texto_historial
        )

        self.historial = QListWidget()

        self.historial.setFocusPolicy(
            Qt.NoFocus
        )

        principal.addWidget(
            self.historial
        )

    # =====================================================
    # TIPO DE BOTON
    # =====================================================

    def tipo_boton(self, texto):

        if texto == "=":
            return "igual"

        if texto in ["+", "-", "×", "÷"]:
            return "operador"

        if texto == "C":
            return "limpiar"

        if texto in ["(", ")"]:
            return "especial"

        return "numero"

    # =====================================================
    # DISEÑO
    # =====================================================

    def dar_estilo(self):

        estilo = """

        QMainWindow {
            background-color: #171717;
        }

        QLabel[tipo="titulo"] {
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
            padding: 5px;
        }

        QLabel[tipo="subtitulo"] {
            color: #aaaaaa;
            font-size: 12px;
            font-weight: bold;
            padding-top: 5px;
        }

        QLineEdit {
            background-color: #252525;
            color: #7dd3fc;
            border: 2px solid #3d3d3d;
            border-radius: 10px;
            font-size: 27px;
            font-weight: bold;
            padding: 10px;
        }

        QListWidget {
            background-color: #252525;
            color: #dddddd;
            border: 1px solid #3d3d3d;
            border-radius: 8px;
            padding: 5px;
            font-size: 12px;
        }

        QPushButton {
            border: none;
            border-radius: 9px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton[categoria="numero"] {
            background-color: #333333;
            color: #ffffff;
        }

        QPushButton[categoria="numero"]:hover {
            background-color: #444444;
        }

        QPushButton[categoria="operador"] {
            background-color: #6c5ce7;
            color: white;
        }

        QPushButton[categoria="operador"]:hover {
            background-color: #8175ed;
        }

        QPushButton[categoria="limpiar"] {
            background-color: #e74c3c;
            color: white;
        }

        QPushButton[categoria="limpiar"]:hover {
            background-color: #ef6658;
        }

        QPushButton[categoria="especial"] {
            background-color: #555555;
            color: white;
        }

        QPushButton[categoria="especial"]:hover {
            background-color: #666666;
        }

        QPushButton[categoria="igual"] {
            background-color: #16a085;
            color: white;
        }

        QPushButton[categoria="igual"]:hover {
            background-color: #1abc9c;
        }

        QPushButton:pressed {
            background-color: #777777;
        }
        """

        self.setStyleSheet(estilo)

    # =====================================================
    # RECIBIR BOTON
    # =====================================================

    def recibir(self, valor):

        if valor == "C":

            self.limpiar_pantalla()

            return

        if valor == "=":

            self.calcular()

            return

        if self.nuevo_calculo:

            if valor in "0123456789.":

                self.expresion = ""

            self.nuevo_calculo = False

        self.expresion += valor

        self.display.setText(
            self.expresion
        )

    # =====================================================
    # CALCULAR
    # =====================================================

    def calcular(self):

        if not self.expresion:
            return

        expresion_real = (
            self.expresion
            .replace("÷", "/")
            .replace("×", "*")
            .replace("x", "*")
        )

        try:

            resultado = MotorCalculo.ejecutar(
                expresion_real
            )

            if (
                isinstance(resultado, float)
                and resultado.is_integer()
            ):

                resultado = int(resultado)

            resultado = str(resultado)

            registro = (
                self.expresion
                + " = "
                + resultado
            )

            self.historial.addItem(
                registro
            )

            while (
                self.historial.count()
                > self.MAX_OPERACIONES
            ):

                self.historial.takeItem(0)

            self.historial.scrollToBottom()

            self.display.setText(
                resultado
            )

            self.expresion = resultado
            self.nuevo_calculo = True

        except ZeroDivisionError:

            self.display.setText(
                "Error: división / 0"
            )

            self.expresion = ""
            self.nuevo_calculo = False

        except Exception:

            self.display.setText(
                "Error de sintaxis"
            )

            self.expresion = ""
            self.nuevo_calculo = False

    # =====================================================
    # LIMPIAR PANTALLA
    # =====================================================

    def limpiar_pantalla(self):

        self.expresion = ""

        self.display.clear()

        self.nuevo_calculo = False

    # =====================================================
    # COPIAR RESULTADO
    # =====================================================

    def copiar(self):

        texto = self.display.text()

        if texto and not texto.startswith("Error"):

            QApplication.clipboard().setText(texto)

    # =====================================================
    # INFORMACION
    # =====================================================

    def mostrar_informacion(self):

        QMessageBox.information(
            self,
            "Información",
            "Funciones disponibles:\n\n"
            "• Suma\n"
            "• Resta\n"
            "• Multiplicación\n"
            "• División\n"
            "• Paréntesis\n"
            "• Decimales\n"
            "• Historial\n"
            "• Atajos de teclado"
        )

    # =====================================================
    # TECLADO
    # =====================================================

    def keyPressEvent(self, evento):

        tecla = evento.key()
        texto = evento.text()

        if tecla in (
            Qt.Key_Return,
            Qt.Key_Enter
        ):

            self.recibir("=")

        elif tecla in (
            Qt.Key_Escape,
            Qt.Key_Backspace
        ):

            self.recibir("C")

        elif texto in "0123456789+-./*()":

            conversion = {
                "*": "×",
                "/": "÷"
            }

            self.recibir(
                conversion.get(
                    texto,
                    texto
                )
            )

        else:

            super().keyPressEvent(evento)


# =========================================================
# EJECUTAR PROGRAMA
# =========================================================

def iniciar():

    programa = QApplication(sys.argv)

    ventana = Calculadora()

    ventana.show()

    sys.exit(
        programa.exec()
    )


if __name__ == "__main__":
    iniciar()