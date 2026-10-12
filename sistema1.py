
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QCheckBox, QRadioButton,
    QVBoxLayout, QHBoxLayout, QButtonGroup
)


class VentanaTexto(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador de Texto")
        self.setFixedSize(500, 450)

        self.crear_interfaz()

    def crear_interfaz(self):

        principal = QVBoxLayout()

        titulo = QLabel("Escriba un texto:")
        principal.addWidget(titulo)

        self.campo = QLineEdit()
        self.campo.setPlaceholderText("Ingrese aquí su texto...")
        principal.addWidget(self.campo)

        principal.addWidget(QLabel("Elija una operación:"))

        self.operaciones = QComboBox()
        self.operaciones.addItems([
            "Contar Caracteres",
            "Contar Palabras",
            "Convertir a Mayúsculas",
            "Invertir Texto"
        ])
        principal.addWidget(self.operaciones)

        self.espacios = QCheckBox("Contar también los espacios")
        principal.addWidget(self.espacios)

        principal.addWidget(QLabel("¿Desea guardar el resultado?"))

        opciones = QHBoxLayout()

        self.guardar = QRadioButton("Sí")
        self.no_guardar = QRadioButton("No")

        self.guardar.setChecked(True)

        grupo = QButtonGroup(self)
        grupo.addButton(self.guardar)
        grupo.addButton(self.no_guardar)

        opciones.addWidget(self.guardar)
        opciones.addWidget(self.no_guardar)

        principal.addLayout(opciones)

        self.boton = QPushButton("Procesar texto")
        self.boton.clicked.connect(self.ejecutar)
        principal.addWidget(self.boton)

        self.resultado = QLabel("Resultado: -")
        self.resultado.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )
        principal.addWidget(self.resultado)

        principal.addWidget(QLabel("Historial de operaciones:"))

        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        principal.addWidget(self.historial)

        self.setLayout(principal)

    def ejecutar(self):

        texto = self.campo.text()
        operacion = self.operaciones.currentText()

        if operacion == "Contar Caracteres":

            if self.espacios.isChecked():
                cantidad = len(texto)
            else:
                cantidad = len(texto.replace(" ", ""))

            respuesta = "Cantidad de caracteres: " + str(cantidad)

        elif operacion == "Contar Palabras":

            lista = texto.split()
            respuesta = "Cantidad de palabras: " + str(len(lista))

        elif operacion == "Convertir a Mayúsculas":

            respuesta = "Texto: " + texto.upper()

        else:

            respuesta = "Texto invertido: " + texto[::-1]

        self.resultado.setText("Resultado: " + respuesta)

        if self.guardar.isChecked():
            registro = (
                "[" + operacion + "] "
                + texto + " -> "
                + respuesta
            )
            self.historial.append(registro)


if __name__ == "__main__":

    aplicacion = QApplication(sys.argv)

    ventana = VentanaTexto()
    ventana.show()

    sys.exit(aplicacion.exec())