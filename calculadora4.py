import ast
import math
import operator
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
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

# ============================================================

# EVALUADOR MATEMÁTICO

# ============================================================

class Evaluador:


operadores = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}

CONSTANTES = {
    "pi": math.pi,
    "e": math.e
}

FUNCIONES = {
    "sqrt": math.sqrt,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil
}

@classmethod
def evaluar(cls, expresion, grados=True):

    expresion = expresion.strip()

    expresion = expresion.replace("×", "*")
    expresion = expresion.replace("÷", "/")
    expresion = expresion.replace("^", "**")
    expresion = expresion.replace("π", "pi")

    abiertos = expresion.count("(")
    cerrados = expresion.count(")")

    if abiertos > cerrados:
        expresion += ")" * (abiertos - cerrados)

    if not expresion:
        raise ValueError("Expresión vacía")

    try:
        arbol = ast.parse(
            expresion,
            mode="eval"
        )

        return cls.procesar(
            arbol.body,
            grados
        )

    except ZeroDivisionError:
        raise

    except ValueError:
        raise

    except Exception:
        raise ValueError(
            "Expresión inválida"
        )

@classmethod
def procesar(cls, nodo, grados):

    # ----------------------------------------------------
    # NÚMEROS
    # ----------------------------------------------------

    if isinstance(nodo, ast.Constant):

        if isinstance(
            nodo.value,
            (int, float)
        ):
            return nodo.value

        raise ValueError(
            "Número no permitido"
        )

    # ----------------------------------------------------
    # CONSTANTES
    # ----------------------------------------------------

    if isinstance(nodo, ast.Name):

        nombre = nodo.id

        if nombre in cls.CONSTANTES:
            return cls.CONSTANTES[nombre]

        raise ValueError(
            "Constante desconocida"
        )

    # ----------------------------------------------------
    # OPERACIONES
    # ----------------------------------------------------

    if isinstance(nodo, ast.BinOp):

        izquierda = cls.procesar(
            nodo.left,
            grados
        )

        derecha = cls.procesar(
            nodo.right,
            grados
        )

        operador = type(nodo.op)

        if operador not in cls.OPERADORES:
            raise ValueError(
                "Operador no permitido"
            )

        return cls.OPERADORES[operador](
            izquierda,
            derecha
        )

    # ----------------------------------------------------
    # OPERACIONES UNARIAS
    # ----------------------------------------------------

    if isinstance(nodo, ast.UnaryOp):

        valor = cls.procesar(
            nodo.operand,
            grados
        )

        operador = type(nodo.op)

        if operador not in cls.OPERADORES:
            raise ValueError(
                "Operador no permitido"
            )

        return cls.OPERADORES[operador](valor)

    # ----------------------------------------------------
    # FUNCIONES
    # ----------------------------------------------------

    if isinstance(nodo, ast.Call):

        if not isinstance(
            nodo.func,
            ast.Name
        ):
            raise ValueError(
                "Función inválida"
            )

        nombre = nodo.func.id

        if len(nodo.args) != 1:
            raise ValueError(
                "La función necesita un argumento"
            )

        argumento = cls.procesar(
            nodo.args[0],
            grados
        )

        # Trigonometría normal

        if nombre == "sin":

            if grados:
                argumento = math.radians(
                    argumento
                )

            return math.sin(argumento)

        if nombre == "cos":

            if grados:
                argumento = math.radians(
                    argumento
                )

            return math.cos(argumento)

        if nombre == "tan":

            if grados:
                argumento = math.radians(
                    argumento
                )

            return math.tan(argumento)

        # Trigonometría inversa

        if nombre == "asin":

            resultado = math.asin(
                argumento
            )

            return (
                math.degrees(resultado)
                if grados
                else resultado
            )

        if nombre == "acos":

            resultado = math.acos(
                argumento
            )

            return (
                math.degrees(resultado)
                if grados
                else resultado
            )

        if nombre == "atan":

            resultado = math.atan(
                argumento
            )

            return (
                math.degrees(resultado)
                if grados
                else resultado
            )

        # Logaritmos

        if nombre == "log":
            return math.log10(argumento)

        if nombre == "ln":
            return math.log(argumento)

        # Otras funciones

        if nombre in cls.FUNCIONES:
            return cls.FUNCIONES[nombre](
                argumento
            )

        raise ValueError(
            "Función no disponible"
        )

    raise ValueError(
        "Operación no permitida"
    )


# ============================================================

# VENTANA PRINCIPAL

# ============================================================

class CalculadoraCientifica(QMainWindow):

LIMITE_HISTORIAL = 10

def __init__(self):

    super().__init__()

    self.expresion = ""
    self.resultado_nuevo = False
    self.modo_grados = True

    self.configurar_ventana()
    self.construir_menu()
    self.construir_interfaz()
    self.configurar_estilos()

# ========================================================
# CONFIGURACIÓN
# ========================================================

def configurar_ventana(self):

    self.setWindowTitle(
        "Calculadora Científica"
    )

    self.setFixedSize(
        460,
        720
    )

# ========================================================
# MENÚS
# ========================================================

def construir_menu(self):

    barra = self.menuBar()

    # ARCHIVO

    menu_archivo = barra.addMenu(
        "Archivo"
    )

    accion_nueva = QAction(
        "Nueva operación",
        self
    )

    accion_nueva.setShortcut(
        QKeySequence("Ctrl+N")
    )

    accion_nueva.triggered.connect(
        self.nueva_operacion
    )

    menu_archivo.addAction(
        accion_nueva
    )

    menu_archivo.addSeparator()

    accion_salir = QAction(
        "Salir",
        self
    )

    accion_salir.setShortcut(
        QKeySequence("Ctrl+Q")
    )

    accion_salir.triggered.connect(
        self.close
    )

    menu_archivo.addAction(
        accion_salir
    )

    # EDITAR

    menu_editar = barra.addMenu(
        "Editar"
    )

    accion_copiar = QAction(
        "Copiar resultado",
        self
    )

    accion_copiar.setShortcut(
        QKeySequence("Ctrl+C")
    )

    accion_copiar.triggered.connect(
        self.copiar_resultado
    )

    menu_editar.addAction(
        accion_copiar
    )

    accion_limpiar = QAction(
        "Limpiar todo",
        self
    )

    accion_limpiar.triggered.connect(
        self.reiniciar
    )

    menu_editar.addAction(
        accion_limpiar
    )

    # MODO

    menu_modo = barra.addMenu(
        "Modo"
    )

    self.accion_grados = QAction(
        "Grados",
        self
    )

    self.accion_grados.setCheckable(
        True
    )

    self.accion_grados.setChecked(
        True
    )

    self.accion_grados.triggered.connect(
        self.seleccionar_grados
    )

    menu_modo.addAction(
        self.accion_grados
    )

    self.accion_radianes = QAction(
        "Radianes",
        self
    )

    self.accion_radianes.setCheckable(
        True
    )

    self.accion_radianes.triggered.connect(
        self.seleccionar_radianes
    )

    menu_modo.addAction(
        self.accion_radianes
    )

    # AYUDA

    menu_ayuda = barra.addMenu(
        "Ayuda"
    )

    accion_acerca = QAction(
        "Acerca de",
        self
    )

    accion_acerca.triggered.connect(
        self.acerca_de
    )

    menu_ayuda.addAction(
        accion_acerca
    )

    accion_funciones = QAction(
        "Funciones disponibles",
        self
    )

    accion_funciones.triggered.connect(
        self.lista_funciones
    )

    menu_ayuda.addAction(
        accion_funciones
    )

# ========================================================
# INTERFAZ
# ========================================================

def construir_interfaz(self):

    contenedor = QWidget()

    self.setCentralWidget(
        contenedor
    )

    principal = QVBoxLayout(
        contenedor
    )

    principal.setContentsMargins(
        18,
        18,
        18,
        18
    )

    principal.setSpacing(8)

    titulo = QLabel(
        "◆ CALCULADORA CIENTÍFICA"
    )

    titulo.setProperty(
        "tipo",
        "titulo"
    )

    principal.addWidget(
        titulo
    )

    self.indicador_modo = QLabel(
        "MODO: GRADOS"
    )

    self.indicador_modo.setProperty(
        "tipo",
        "modo"
    )

    principal.addWidget(
        self.indicador_modo
    )

    # PANTALLA

    self.display = QLineEdit()

    self.display.setReadOnly(
        True
    )

    self.display.setAlignment(
        Qt.AlignRight
    )

    self.display.setPlaceholderText(
        "0"
    )

    principal.addWidget(
        self.display
    )

    # BOTONES CIENTÍFICOS

    panel_cientifico = QGridLayout()

    panel_cientifico.setSpacing(6)

    cientificos = [
        "sin",
        "cos",
        "tan",
        "√",
        "asin",
        "acos",
        "atan",
        "x²",
        "log",
        "ln",
        "π",
        "e"
    ]

    for indice, nombre in enumerate(
        cientificos
    ):

        fila = indice // 4
        columna = indice % 4

        boton = QPushButton(
            nombre
        )

        boton.setMinimumHeight(
            38
        )

        boton.setProperty(
            "tipo",
            "cientifico"
        )

        boton.clicked.connect(
            lambda _, valor=nombre:
            self.agregar(valor)
        )

        panel_cientifico.addWidget(
            boton,
            fila,
            columna
        )

    principal.addLayout(
        panel_cientifico
    )

    # TECLADO PRINCIPAL

    panel_teclado = QGridLayout()

    panel_teclado.setSpacing(7)

    teclas = [
        "C", "⌫", "(", ")",
        "7", "8", "9", "÷",
        "4", "5", "6", "×",
        "1", "2", "3", "-",
        "0", ".", "^", "+",
        "%", "CE", "=", ""
    ]

    for indice, tecla in enumerate(
        teclas
    ):

        if tecla == "":
            continue

        fila = indice // 4
        columna = indice % 4

        boton = QPushButton(
            tecla
        )

        boton.setMinimumHeight(
            44
        )

        if tecla in (
            "+",
            "-",
            "×",
            "÷",
            "^"
        ):
            categoria = "operador"

        elif tecla == "=":
            categoria = "igual"

        elif tecla in (
            "C",
            "CE",
            "⌫",
            "(",
            ")",
            "%"
        ):
            categoria = "accion"

        else:
            categoria = "numero"

        boton.setProperty(
            "tipo",
            categoria
        )

        boton.clicked.connect(
            lambda _, valor=tecla:
            self.agregar(valor)
        )

        panel_teclado.addWidget(
            boton,
            fila,
            columna
        )

    principal.addLayout(
        panel_teclado
    )

    # HISTORIAL

    etiqueta_historial = QLabel(
        "📋 Historial"
    )

    etiqueta_historial.setProperty(
        "tipo",
        "subtitulo"
    )

    principal.addWidget(
        etiqueta_historial
    )

    self.lista_historial = QListWidget()

    self.lista_historial.setFocusPolicy(
        Qt.NoFocus
    )

    principal.addWidget(
        self.lista_historial
    )

# ========================================================
# ESTILOS
# ========================================================

def configurar_estilos(self):

    self.setStyleSheet("""

    QMainWindow {
        background-color: #111827;
    }

    QMenuBar {
        background-color: #1f2937;
        color: white;
    }

    QMenuBar::item {
        padding: 6px 12px;
    }

    QMenuBar::item:selected {
        background-color: #374151;
    }

    QMenu {
        background-color: #1f2937;
        color: white;
    }

    QMenu::item {
        padding: 7px 25px;
    }

    QMenu::item:selected {
        background-color: #2563eb;
    }

    QLabel[tipo="titulo"] {
        color: #60a5fa;
        font-size: 17px;
        font-weight: bold;
    }

    QLabel[tipo="modo"] {
        color: #34d399;
        font-size: 10px;
        font-weight: bold;
    }

    QLabel[tipo="subtitulo"] {
        color: #9ca3af;
        font-weight: bold;
    }

    QLineEdit {
        background-color: #1f2937;
        color: white;
        border: 2px solid #374151;
        border-radius: 10px;
        font-size: 28px;
        font-weight: bold;
        padding: 10px;
        min-height: 45px;
    }

    QPushButton {
        border: none;
        border-radius: 8px;
        font-size: 15px;
        font-weight: bold;
    }

    QPushButton[tipo="numero"] {
        background-color: #374151;
        color: white;
    }

    QPushButton[tipo="numero"]:hover {
        background-color: #4b5563;
    }

    QPushButton[tipo="operador"] {
        background-color: #2563eb;
        color: white;
    }

    QPushButton[tipo="operador"]:hover {
        background-color: #1d4ed8;
    }

    QPushButton[tipo="accion"] {
        background-color: #dc2626;
        color: white;
    }

    QPushButton[tipo="accion"]:hover {
        background-color: #b91c1c;
    }

    QPushButton[tipo="igual"] {
        background-color: #059669;
        color: white;
    }

    QPushButton[tipo="igual"]:hover {
        background-color: #047857;
    }

    QPushButton[tipo="cientifico"] {
        background-color: #4b5563;
        color: #bfdbfe;
    }

    QListWidget {
        background-color: #1f2937;
        color: #d1d5db;
        border: 1px solid #374151;
        border-radius: 8px;
    }

    """)

# ========================================================
# MANEJO DE BOTONES
# ========================================================

def agregar(self, valor):

    if valor in ("C", "CE"):
        self.limpiar_pantalla()
        return

    if valor == "⌫":

        self.expresion = self.expresion[:-1]

        self.display.setText(
            self.expresion
        )

        return

    if valor == "=":
        self.calcular_resultado()
        return

    funciones = (
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "log",
        "ln"
    )

    if valor in funciones:

        if (
            self.resultado_nuevo
            or not self.expresion
        ):
            self.expresion = ""

        self.expresion += (
            valor + "("
        )

        self.resultado_nuevo = False

        self.display.setText(
            self.expresion
        )

        return

    if valor == "√":

        self.expresion += "sqrt("
        self.resultado_nuevo = False

        self.display.setText(
            self.expresion
        )

        return

    if valor == "x²":

        if self.expresion:
            self.expresion += "^2"

            self.display.setText(
                self.expresion
            )

        return

    if valor == "π":

        if self.resultado_nuevo:
            self.expresion = ""

        self.expresion += "π"
        self.resultado_nuevo = False

        self.display.setText(
            self.expresion
        )

        return

    if valor == "e":

        if self.resultado_nuevo:
            self.expresion = ""

        self.expresion += "e"
        self.resultado_nuevo = False

        self.display.setText(
            self.expresion
        )

        return

    if (
        self.resultado_nuevo
        and valor in "0123456789."
    ):
        self.expresion = ""

    self.resultado_nuevo = False

    self.expresion += valor

    self.display.setText(
        self.expresion
    )

# ========================================================
# CÁLCULO
# ========================================================

def calcular_resultado(self):

    if not self.expresion:
        return

    try:

        resultado = Evaluador.evaluar(
            self.expresion,
            self.modo_grados
        )

        if isinstance(
            resultado,
            float
        ):

            if resultado.is_integer():
                resultado = int(
                    resultado
                )
            else:
                resultado = round(
                    resultado,
                    12
                )

        texto = str(
            resultado
        )

        self.lista_historial.addItem(
            f"{self.expresion} = {texto}"
        )

        while (
            self.lista_historial.count()
            > self.LIMITE_HISTORIAL
        ):
            self.lista_historial.takeItem(0)

        self.lista_historial.scrollToBottom()

        self.display.setText(
            texto
        )

        self.expresion = texto
        self.resultado_nuevo = True

    except ZeroDivisionError:

        self.display.setText(
            "Error: división por 0"
        )

        self.expresion = ""

    except ValueError:

        self.display.setText(
            "Error de sintaxis"
        )

        self.expresion = ""

    except OverflowError:

        self.display.setText(
            "Número demasiado grande"
        )

        self.expresion = ""

    except Exception:

        self.display.setText(
            "Error"
        )

        self.expresion = ""

# ========================================================
# LIMPIEZA
# ========================================================

def limpiar_pantalla(self):

    self.expresion = ""
    self.display.clear()
    self.resultado_nuevo = False

def nueva_operacion(self):

    self.limpiar_pantalla()
    self.lista_historial.clear()

def reiniciar(self):

    self.nueva_operacion()

# ========================================================
# COPIAR
# ========================================================

def copiar_resultado(self):

    texto = self.display.text()

    if texto:
        QApplication.clipboard().setText(
            texto
        )

# ========================================================
# MODOS
# ========================================================

def seleccionar_grados(self):

    self.modo_grados = True

    self.accion_grados.setChecked(
        True
    )

    self.accion_radianes.setChecked(
        False
    )

    self.indicador_modo.setText(
        "MODO: GRADOS"
    )

def seleccionar_radianes(self):

    self.modo_grados = False

    self.accion_grados.setChecked(
        False
    )

    self.accion_radianes.setChecked(
        True
    )

    self.indicador_modo.setText(
        "MODO: RADIANES"
    )

# ========================================================
# INFORMACIÓN
# ========================================================

def acerca_de(self):

    QMessageBox.information(
        self,
        "Acerca de",
        "CALCULADORA CIENTÍFICA\n\n"
        "Desarrollada por:\n"
        "JOSE ARMANDO GUZMAN\n\n"
        "Desarrollada con Python y PySide6.\n\n"
        "Incluye:\n"
        "• Operaciones básicas\n"
        "• Potencias\n"
        "• Porcentajes\n"
        "• Trigonometría\n"
        "• Logaritmos\n"
        "• Constantes π y e\n"
        "• Historial\n"
        "• Grados y radianes\n"
        "• Evaluación segura"
    )

def lista_funciones(self):

    QMessageBox.information(
        self,
        "Funciones disponibles",
        "OPERACIONES:\n\n"
        "+  Suma\n"
        "-  Resta\n"
        "×  Multiplicación\n"
        "÷  División\n"
        "^  Potencia\n"
        "%  Módulo\n\n"
        "FUNCIONES:\n\n"
        "sin(x)\n"
        "cos(x)\n"
        "tan(x)\n"
        "asin(x)\n"
        "acos(x)\n"
        "atan(x)\n"
        "sqrt(x)\n"
        "log(x)\n"
        "ln(x)\n\n"
        "CONSTANTES:\n\n"
        "π\n"
        "e"
    )

# ========================================================
# TECLADO
# ========================================================

def keyPressEvent(self, evento):

    tecla = evento.key()
    caracter = evento.text()

    if tecla in (
        Qt.Key_Return,
        Qt.Key_Enter
    ):
        self.agregar("=")
        return

    if tecla == Qt.Key_Backspace:
        self.agregar("⌫")
        return

    if tecla == Qt.Key_Escape:
        self.agregar("C")
        return

    if caracter in "0123456789":
        self.agregar(caracter)
        return

    if caracter in "+-().":
        self.agregar(caracter)
        return

    if caracter == "*":
        self.agregar("×")
        return

    if caracter == "/":
        self.agregar("÷")
        return

    if caracter == "^":
        self.agregar("^")
        return

    super().keyPressEvent(evento)

# ============================================================

# EJECUCIÓN

# ============================================================

def ejecutar():

app = QApplication(
    sys.argv
)

ventana = CalculadoraCientifica()

ventana.show()

sys.exit(
    app.exec()
)

if **name** == "**main**":
ejecutar()