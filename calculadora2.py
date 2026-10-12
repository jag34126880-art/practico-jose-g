

import tkinter as tk
from tkinter import messagebox
import ast
import operator


# ---------------------------------------------------------
# CLASE PARA REALIZAR LOS CÁLCULOS DE FORMA SEGURA
# ---------------------------------------------------------

class CalculadoraSegura:

    operaciones = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg
    }

    @classmethod
    def resolver(cls, expresion):

        # Completar paréntesis que hayan quedado abiertos
        abiertos = expresion.count("(")
        cerrados = expresion.count(")")

        if abiertos > cerrados:
            expresion += ")" * (abiertos - cerrados)

        try:
            arbol = ast.parse(expresion, mode="eval")
            return cls.procesar(arbol.body)

        except ZeroDivisionError:
            raise ZeroDivisionError

        except Exception:
            raise ValueError("Expresión incorrecta")

    @classmethod
    def procesar(cls, nodo):

        # Números
        if isinstance(nodo, ast.Constant):

            if isinstance(nodo.value, (int, float)):
                return nodo.value

            raise ValueError()

        # Operaciones
        if isinstance(nodo, ast.BinOp):

            numero1 = cls.procesar(nodo.left)
            numero2 = cls.procesar(nodo.right)

            tipo = type(nodo.op)

            if tipo in cls.operaciones:
                return cls.operaciones[tipo](
                    numero1,
                    numero2
                )

        # Números positivos o negativos
        if isinstance(nodo, ast.UnaryOp):

            numero = cls.procesar(nodo.operand)
            tipo = type(nodo.op)

            if tipo in cls.operaciones:
                return cls.operaciones[tipo](numero)

        raise ValueError()


# ---------------------------------------------------------
# CLASE PRINCIPAL DE LA CALCULADORA
# ---------------------------------------------------------

class CalculadoraApp:

    def __init__(self, ventana):

        self.ventana = ventana

        # Guarda la operación actual
        self.operacion = ""

        # Indica si acabamos de obtener un resultado
        self.resultado_obtenido = False

        # Número máximo de operaciones guardadas
        self.max_historial = 5

        self.configurar_ventana()
        self.crear_interfaz()
        self.configurar_teclado()

    # -----------------------------------------------------
    # CONFIGURACIÓN DE LA VENTANA
    # -----------------------------------------------------

    def configurar_ventana(self):

        self.ventana.title("Calculadora")
        self.ventana.geometry("380x570")
        self.ventana.resizable(False, False)

        self.ventana.configure(
            bg="#181a1b"
        )

    # -----------------------------------------------------
    # CREAR INTERFAZ
    # -----------------------------------------------------

    def crear_interfaz(self):

        # Título
        titulo = tk.Label(
            self.ventana,
            text="CALCULADORA",
            font=("Arial", 16, "bold"),
            bg="#181a1b",
            fg="#ffffff"
        )

        titulo.pack(pady=(18, 8))

        # Pantalla
        self.pantalla = tk.Entry(
            self.ventana,
            font=("Arial", 26, "bold"),
            justify="right",
            bg="#25282a",
            fg="#ffffff",
            insertbackground="white",
            relief="flat"
        )

        self.pantalla.pack(
            padx=20,
            pady=10,
            ipady=14,
            fill="x"
        )

        # Marco de botones
        marco_botones = tk.Frame(
            self.ventana,
            bg="#181a1b"
        )

        marco_botones.pack(
            padx=18,
            pady=10
        )

        # Configuración de filas y columnas
        for fila in range(5):
            marco_botones.rowconfigure(
                fila,
                weight=1
            )

        for columna in range(4):
            marco_botones.columnconfigure(
                columna,
                weight=1
            )

        # Botones
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

        for texto, fila, columna in botones:

            color = self.obtener_color(texto)

            boton = tk.Button(
                marco_botones,
                text=texto,
                font=("Arial", 15, "bold"),
                width=6,
                height=2,
                bg=color,
                fg="white",
                activebackground="#777777",
                activeforeground="white",
                relief="flat",
                bd=0,
                command=lambda x=texto:
                    self.pulsar_boton(x)
            )

            if texto == "=":

                boton.grid(
                    row=fila,
                    column=columna,
                    columnspan=2,
                    padx=4,
                    pady=4,
                    sticky="nsew"
                )

            else:

                boton.grid(
                    row=fila,
                    column=columna,
                    padx=4,
                    pady=4,
                    sticky="nsew"
                )

        # Título del historial
        historial_titulo = tk.Label(
            self.ventana,
            text="Últimas operaciones",
            font=("Arial", 11, "bold"),
            bg="#181a1b",
            fg="#b8b8b8"
        )

        historial_titulo.pack(
            anchor="w",
            padx=20,
            pady=(8, 4)
        )

        # Historial
        self.historial = tk.Listbox(
            self.ventana,
            height=5,
            font=("Consolas", 10),
            bg="#25282a",
            fg="#ffffff",
            selectbackground="#444444",
            relief="flat",
            bd=0
        )

        self.historial.pack(
            padx=20,
            fill="x"
        )

    # -----------------------------------------------------
    # COLORES DE LOS BOTONES
    # -----------------------------------------------------

    def obtener_color(self, texto):

        if texto == "C":
            return "#d64545"

        if texto in ["+", "-", "×", "÷"]:
            return "#e58e26"

        if texto == "=":
            return "#2878d7"

        if texto in ["(", ")"]:
            return "#55595d"

        return "#303438"

    # -----------------------------------------------------
    # BOTONES
    # -----------------------------------------------------

    def pulsar_boton(self, valor):

        # Limpiar
        if valor == "C":

            self.operacion = ""
            self.pantalla.delete(0, tk.END)
            self.resultado_obtenido = False

            return

        # Calcular
        if valor == "=":

            self.mostrar_resultado()

            return

        # Si se obtuvo un resultado y se pulsa un número,
        # comenzar una nueva operación
        if self.resultado_obtenido:

            if valor in "0123456789.":

                self.operacion = ""

            self.resultado_obtenido = False

        # Agregar el botón a la operación
        self.operacion += valor

        self.actualizar_pantalla()

    # -----------------------------------------------------
    # ACTUALIZAR PANTALLA
    # -----------------------------------------------------

    def actualizar_pantalla(self):

        self.pantalla.delete(
            0,
            tk.END
        )

        self.pantalla.insert(
            0,
            self.operacion
        )

    # -----------------------------------------------------
    # CALCULAR RESULTADO
    # -----------------------------------------------------

    def mostrar_resultado(self):

        if not self.operacion:
            return

        # Convertir símbolos de la calculadora
        expresion = self.operacion

        expresion = expresion.replace(
            "×",
            "*"
        )

        expresion = expresion.replace(
            "÷",
            "/"
        )

        try:

            resultado = CalculadoraSegura.resolver(
                expresion
            )

            # Mostrar números enteros sin .0
            if isinstance(resultado, float):

                if resultado.is_integer():
                    resultado = int(resultado)

            resultado = str(resultado)

            # Guardar en historial
            texto_historial = (
                self.operacion
                + " = "
                + resultado
            )

            self.historial.insert(
                tk.END,
                texto_historial
            )

            # Mantener solamente 5 operaciones
            if self.historial.size() > self.max_historial:

                self.historial.delete(0)

            # Mostrar resultado
            self.operacion = resultado

            self.pantalla.delete(
                0,
                tk.END
            )

            self.pantalla.insert(
                0,
                resultado
            )

            self.resultado_obtenido = True

        except ZeroDivisionError:

            messagebox.showerror(
                "Error",
                "No se puede dividir entre cero."
            )

            self.limpiar_calculadora()

        except Exception:

            messagebox.showwarning(
                "Error",
                "La operación no es válida."
            )

            self.limpiar_calculadora()

    # -----------------------------------------------------
    # LIMPIAR CALCULADORA
    # -----------------------------------------------------

    def limpiar_calculadora(self):

        self.operacion = ""

        self.pantalla.delete(
            0,
            tk.END
        )

        self.resultado_obtenido = False

    # -----------------------------------------------------
    # TECLADO
    # -----------------------------------------------------

    def configurar_teclado(self):

        self.ventana.bind(
            "<Key>",
            self.tecla_presionada
        )

    def tecla_presionada(self, evento):

        tecla = evento.char

        # Enter
        if evento.keysym in [
            "Return",
            "KP_Enter"
        ]:

            self.pulsar_boton("=")

        # Escape
        elif evento.keysym == "Escape":

            self.pulsar_boton("C")

        # Backspace
        elif evento.keysym == "BackSpace":

            self.pulsar_boton("C")

        # Números y operaciones
        elif tecla in "0123456789+-./*()":

            equivalencias = {
                "*": "×",
                "/": "÷"
            }

            valor = equivalencias.get(
                tecla,
                tecla
            )

            self.pulsar_boton(valor)


# ---------------------------------------------------------
# INICIO DEL PROGRAMA
# ---------------------------------------------------------

if __name__ == "__main__":

    ventana = tk.Tk()

    programa = CalculadoraApp(
        ventana
    )

    ventana.mainloop()