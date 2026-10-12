
import tkinter as tk
from tkinter import ttk, messagebox


class InventarioApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("1150x730")
        self.root.configure(bg="#111827")

        self.lista_productos = []
        self.producto_editando = None

        self.construir_ventana()

    # -------------------------------------------------
    # CREACIÓN DE LA INTERFAZ
    # -------------------------------------------------

    def construir_ventana(self):

        principal = tk.Frame(
            self.root,
            bg="#111827"
        )
        principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ENCABEZADO
        encabezado = tk.Frame(
            principal,
            bg="#111827"
        )
        encabezado.pack(fill="x", pady=(0, 15))

        tk.Label(
            encabezado,
            text="🛒 CONTROL DE INVENTARIO",
            font=("Segoe UI", 24, "bold"),
            bg="#111827",
            fg="#38bdf8"
        ).pack(anchor="w")

        tk.Label(
            encabezado,
            text="Registro y administración de productos",
            font=("Segoe UI", 11),
            bg="#111827",
            fg="#94a3b8"
        ).pack(anchor="w")

        # ÁREA PRINCIPAL
        contenido = tk.Frame(
            principal,
            bg="#111827"
        )
        contenido.pack(
            fill="both",
            expand=True
        )

        contenido.columnconfigure(0, weight=4)
        contenido.columnconfigure(1, weight=6)
        contenido.rowconfigure(0, weight=1)

        self.crear_formulario(contenido)
        self.crear_inventario(contenido)

    # -------------------------------------------------
    # FORMULARIO
    # -------------------------------------------------

    def crear_formulario(self, padre):

        panel = tk.Frame(
            padre,
            bg="#1f2937"
        )
        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        interior = tk.Frame(
            panel,
            bg="#1f2937"
        )
        interior.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18
        )

        tk.Label(
            interior,
            text="📦 Información del producto",
            font=("Segoe UI", 14, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        datos = tk.Frame(
            interior,
            bg="#1f2937"
        )
        datos.pack(fill="x")

        datos.columnconfigure(1, weight=1)

        self.nombre_producto = self.crear_entrada(
            datos, "Nombre:", 0
        )

        self.codigo_producto = self.crear_entrada(
            datos, "Código SKU:", 1
        )

        self.precio_producto = self.crear_entrada(
            datos, "Precio (Bs.):", 2
        )

        tk.Label(
            datos,
            text="Categoría:",
            bg="#1f2937",
            fg="#cbd5e1",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=6
        )

        self.tipo_producto = ttk.Combobox(
            datos,
            state="readonly",
            values=[
                "Electrónica",
                "Hogar",
                "Ropa",
                "Alimentos",
                "Deportes"
            ]
        )

        self.tipo_producto.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=6
        )

        self.tipo_producto.current(0)

        # ESTADO
        tk.Label(
            interior,
            text="Estado",
            font=("Segoe UI", 11, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            anchor="w",
            pady=(18, 5)
        )

        self.estado_producto = tk.StringVar(
            value="Disponible"
        )

        estados = tk.Frame(
            interior,
            bg="#1f2937"
        )
        estados.pack(anchor="w")

        for opcion in [
            "Disponible",
            "Agotado",
            "En reserva"
        ]:

            tk.Radiobutton(
                estados,
                text=opcion,
                value=opcion,
                variable=self.estado_producto,
                bg="#1f2937",
                fg="#e5e7eb",
                selectcolor="#374151",
                activebackground="#1f2937",
                activeforeground="white"
            ).pack(
                side="left",
                padx=(0, 12)
            )

        # CARACTERÍSTICAS
        tk.Label(
            interior,
            text="Características",
            font=("Segoe UI", 11, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            anchor="w",
            pady=(18, 5)
        )

        opciones = tk.Frame(
            interior,
            bg="#1f2937"
        )
        opciones.pack(anchor="w")

        self.es_nuevo = tk.BooleanVar()
        self.tiene_oferta = tk.BooleanVar()
        self.es_destacado = tk.BooleanVar()
        self.tiene_envio = tk.BooleanVar()

        datos_check = [
            ("🆕 Nuevo", self.es_nuevo, 0, 0),
            ("🔥 Oferta", self.tiene_oferta, 0, 1),
            ("⭐ Destacado", self.es_destacado, 1, 0),
            ("🚚 Envío gratis", self.tiene_envio, 1, 1)
        ]

        for texto, variable, fila, columna in datos_check:

            tk.Checkbutton(
                opciones,
                text=texto,
                variable=variable,
                bg="#1f2937",
                fg="#e5e7eb",
                selectcolor="#374151",
                activebackground="#1f2937",
                activeforeground="white"
            ).grid(
                row=fila,
                column=columna,
                sticky="w",
                padx=(0, 20),
                pady=3
            )

        # DESCRIPCIÓN
        tk.Label(
            interior,
            text="Descripción",
            font=("Segoe UI", 11, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            anchor="w",
            pady=(18, 5)
        )

        self.detalle_producto = tk.Text(
            interior,
            height=5,
            bg="#374151",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.detalle_producto.pack(
            fill="x"
        )

        # BOTONES
        botones = tk.Frame(
            interior,
            bg="#1f2937"
        )
        botones.pack(
            fill="x",
            pady=(20, 0)
        )

        self.boton_guardar = self.crear_boton(
            botones,
            "💾 Guardar",
            self.guardar_producto,
            "#10b981"
        )

        self.boton_guardar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        tk.Button(
            botones,
            text="✏ Editar",
            command=self.cargar_producto,
            bg="#3b82f6",
            fg="white",
            relief="flat",
            padx=8,
            pady=8
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        tk.Button(
            botones,
            text="🗑 Eliminar",
            command=self.quitar_producto,
            bg="#ef4444",
            fg="white",
            relief="flat",
            padx=8,
            pady=8
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        tk.Button(
            botones,
            text="🧹 Limpiar",
            command=self.limpiar_formulario,
            bg="#64748b",
            fg="white",
            relief="flat",
            padx=8,
            pady=8
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

    # -------------------------------------------------
    # PANEL DE INVENTARIO
    # -------------------------------------------------

    def crear_inventario(self, padre):

        panel = tk.Frame(
            padre,
            bg="#1f2937"
        )

        panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        encabezado = tk.Frame(
            panel,
            bg="#1f2937"
        )
        encabezado.pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            encabezado,
            text="🔎 Productos registrados",
            font=("Segoe UI", 14, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(anchor="w")

        self.busqueda = tk.Entry(
            encabezado,
            bg="#374151",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        self.busqueda.pack(
            fill="x",
            pady=(10, 0),
            ipady=6
        )

        self.busqueda.bind(
            "<KeyRelease>",
            lambda evento: self.actualizar_tabla()
        )

        # TABLA
        tabla_contenedor = tk.Frame(
            panel,
            bg="#1f2937"
        )
        tabla_contenedor.pack(
            fill="both",
            expand=True,
            padx=20
        )

        columnas = (
            "producto",
            "sku",
            "precio",
            "categoria",
            "estado"
        )

        self.tabla = ttk.Treeview(
            tabla_contenedor,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        nombres = {
            "producto": "Producto",
            "sku": "SKU",
            "precio": "Precio",
            "categoria": "Categoría",
            "estado": "Estado"
        }

        for columna in columnas:
            self.tabla.heading(
                columna,
                text=nombres[columna]
            )

        self.tabla.column(
            "producto",
            width=150
        )

        self.tabla.column(
            "sku",
            width=90,
            anchor="center"
        )

        self.tabla.column(
            "precio",
            width=90,
            anchor="center"
        )

        self.tabla.column(
            "categoria",
            width=110,
            anchor="center"
        )

        self.tabla.column(
            "estado",
            width=100,
            anchor="center"
        )

        barra = ttk.Scrollbar(
            tabla_contenedor,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=barra.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        self.tabla.bind(
            "<Double-1>",
            lambda evento: self.cargar_producto()
        )

        tk.Button(
            panel,
            text="👁 Consultar producto",
            command=self.mostrar_detalles,
            bg="#8b5cf6",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            pady=10
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

    # -------------------------------------------------
    # FUNCIONES AUXILIARES
    # -------------------------------------------------

    def crear_entrada(self, padre, etiqueta, fila):

        tk.Label(
            padre,
            text=etiqueta,
            bg="#1f2937",
            fg="#cbd5e1",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=6
        )

        entrada = tk.Entry(
            padre,
            bg="#374151",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        entrada.grid(
            row=fila,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=6,
            ipady=4
        )

        return entrada

    def crear_boton(
        self,
        padre,
        texto,
        funcion,
        color
    ):

        return tk.Button(
            padre,
            text=texto,
            command=funcion,
            bg=color,
            fg="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=8
        )

    # -------------------------------------------------
    # REGISTRO
    # -------------------------------------------------

    def guardar_producto(self):

        nombre = self.nombre_producto.get().strip()
        sku = self.codigo_producto.get().strip()
        precio_ingresado = self.precio_producto.get().strip()

        if not nombre:

            messagebox.showwarning(
                "Validación",
                "Debes ingresar el nombre del producto."
            )

            return

        if not sku:

            messagebox.showwarning(
                "Validación",
                "Debes ingresar el código SKU."
            )

            return

        try:

            precio = float(
                precio_ingresado.replace(",", ".")
            )

            if precio < 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Validación",
                "Ingresa un precio válido."
            )

            return

        # Comprobar SKU duplicado
        for posicion, producto in enumerate(
            self.lista_productos
        ):

            if (
                producto["sku"].lower() == sku.lower()
                and posicion != self.producto_editando
            ):

                messagebox.showwarning(
                    "SKU duplicado",
                    "Ese código SKU ya está registrado."
                )

                return

        caracteristicas = []

        if self.es_nuevo.get():
            caracteristicas.append("Nuevo")

        if self.tiene_oferta.get():
            caracteristicas.append("Oferta")

        if self.es_destacado.get():
            caracteristicas.append("Destacado")

        if self.tiene_envio.get():
            caracteristicas.append("Envío gratis")

        nuevo_producto = {
            "nombre": nombre,
            "sku": sku,
            "precio": precio,
            "categoria": self.tipo_producto.get(),
            "estado": self.estado_producto.get(),
            "caracteristicas": ", ".join(
                caracteristicas
            ),
            "descripcion": self.detalle_producto.get(
                "1.0",
                tk.END
            ).strip()
        }

        if self.producto_editando is not None:

            self.lista_productos[
                self.producto_editando
            ] = nuevo_producto

            messagebox.showinfo(
                "Actualización",
                "El producto fue actualizado."
            )

        else:

            self.lista_productos.append(
                nuevo_producto
            )

            messagebox.showinfo(
                "Registro",
                "Producto registrado correctamente."
            )

        self.actualizar_tabla()
        self.limpiar_formulario()

    # -------------------------------------------------
    # MOSTRAR TABLA
    # -------------------------------------------------

    def actualizar_tabla(self):

        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        filtro = self.busqueda.get().lower().strip()

        for indice, producto in enumerate(
            self.lista_productos
        ):

            if (
                filtro in producto["nombre"].lower()
                or filtro in producto["sku"].lower()
            ):

                self.tabla.insert(
                    "",
                    tk.END,
                    iid=str(indice),
                    values=(
                        producto["nombre"],
                        producto["sku"],
                        f"Bs. {producto['precio']:.2f}",
                        producto["categoria"],
                        producto["estado"]
                    )
                )

    # -------------------------------------------------
    # SELECCIÓN
    # -------------------------------------------------

    def obtener_seleccion(self):

        seleccion = self.tabla.selection()

        if not seleccion:
            return None

        return int(seleccion[0])

    # -------------------------------------------------
    # EDITAR
    # -------------------------------------------------

    def cargar_producto(self):

        indice = self.obtener_seleccion()

        if indice is None:

            messagebox.showinfo(
                "Aviso",
                "Selecciona un producto."
            )

            return

        producto = self.lista_productos[indice]

        self.nombre_producto.delete(0, tk.END)
        self.nombre_producto.insert(
            0,
            producto["nombre"]
        )

        self.codigo_producto.delete(0, tk.END)
        self.codigo_producto.insert(
            0,
            producto["sku"]
        )

        self.precio_producto.delete(0, tk.END)
        self.precio_producto.insert(
            0,
            str(producto["precio"])
        )

        self.tipo_producto.set(
            producto["categoria"]
        )

        self.estado_producto.set(
            producto["estado"]
        )

        self.es_nuevo.set(
            "Nuevo" in producto["caracteristicas"]
        )

        self.tiene_oferta.set(
            "Oferta" in producto["caracteristicas"]
        )

        self.es_destacado.set(
            "Destacado" in producto["caracteristicas"]
        )

        self.tiene_envio.set(
            "Envío gratis" in producto["caracteristicas"]
        )

        self.detalle_producto.delete(
            "1.0",
            tk.END
        )

        self.detalle_producto.insert(
            "1.0",
            producto["descripcion"]
        )

        self.producto_editando = indice

        self.boton_guardar.config(
            text="💾 Actualizar"
        )

    # -------------------------------------------------
    # ELIMINAR
    # -------------------------------------------------

    def quitar_producto(self):

        indice = self.obtener_seleccion()

        if indice is None:

            messagebox.showinfo(
                "Aviso",
                "Selecciona un producto."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Quieres eliminar el producto seleccionado?"
        )

        if confirmar:

            self.lista_productos.pop(indice)

            self.actualizar_tabla()
            self.limpiar_formulario()

    # -------------------------------------------------
    # INFORMACIÓN
    # -------------------------------------------------

    def mostrar_detalles(self):

        indice = self.obtener_seleccion()

        if indice is None:

            messagebox.showinfo(
                "Aviso",
                "Selecciona un producto."
            )

            return

        producto = self.lista_productos[indice]

        texto = (
            "INFORMACIÓN DEL PRODUCTO\n\n"
            f"Nombre: {producto['nombre']}\n"
            f"SKU: {producto['sku']}\n"
            f"Precio: Bs. {producto['precio']:.2f}\n"
            f"Categoría: {producto['categoria']}\n"
            f"Estado: {producto['estado']}\n"
            f"Características: "
            f"{producto['caracteristicas'] or 'Ninguna'}\n\n"
            f"Descripción:\n"
            f"{producto['descripcion'] or 'Sin descripción'}"
        )

        messagebox.showinfo(
            "Detalle del producto",
            texto
        )

    # -------------------------------------------------
    # LIMPIAR
    # -------------------------------------------------

    def limpiar_formulario(self):

        self.nombre_producto.delete(
            0,
            tk.END
        )

        self.codigo_producto.delete(
            0,
            tk.END
        )

        self.precio_producto.delete(
            0,
            tk.END
        )

        self.tipo_producto.current(0)

        self.estado_producto.set(
            "Disponible"
        )

        self.es_nuevo.set(False)
        self.tiene_oferta.set(False)
        self.es_destacado.set(False)
        self.tiene_envio.set(False)

        self.detalle_producto.delete(
            "1.0",
            tk.END
        )

        self.producto_editando = None

        self.boton_guardar.config(
            text="💾 Guardar"
        )


if __name__ == "__main__":

    root = tk.Tk()

    programa = InventarioApp(root)

    root.mainloop()