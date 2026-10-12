import customtkinter as ctk
from tkinter import messagebox



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



class FichaEstudiante(ctk.CTkToplevel):

    def __init__(self, padre, datos):
        super().__init__(padre)

        self.title("Detalles de Expediente")
        self.geometry("480x500")
        self.resizable(False, False)

        self.transient(padre)
        self.grab_set()

        # Título
        titulo = ctk.CTkLabel(
            self,
            text="📌 EXPEDIENTE ACADÉMICO",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color="#38bdf8"
        )

        titulo.pack(
            padx=25,
            pady=(25, 15)
        )

        # Contenedor
        tarjeta = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        tarjeta.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        informacion = (
            f"Estudiante:\n"
            f"{datos['nombre']}\n\n"

            f"C.I. / DNI:\n"
            f"{datos['ci']}\n\n"

            f"Nivel / Curso:\n"
            f"{datos['curso']}\n\n"

            f"Jornada:\n"
            f"{datos['turno']}\n\n"

            f"Intereses:\n"
            f"{datos['actividades'] or 'Sin registro'}\n\n"

            f"Observaciones:\n"
            f"{datos['observaciones'] or 'N/A'}"
        )

        texto = ctk.CTkLabel(
            tarjeta,
            text=informacion,
            justify="left",
            anchor="w",
            wraplength=390,
            font=ctk.CTkFont(size=14)
        )

        texto.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # Botón cerrar
        boton_cerrar = ctk.CTkButton(
            self,
            text="Cerrar Ficha",
            command=self.destroy,
            fg_color="#475569",
            hover_color="#334155"
        )

        boton_cerrar.pack(
            padx=25,
            pady=(5, 20)
        )


# ==============================================================================
# APLICACIÓN PRINCIPAL
# ==============================================================================

class GestionEstudiantesApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "EduControl - Gestión Académica"
        )

        self.geometry(
            "1050x700"
        )

        self.minsize(
            950,
            650
        )

        # Datos
        self.expedientes = []

        # Índice que se está editando
        self.id_edicion = None

        self.construir_interfaz()

    # ==========================================================================
    # INTERFAZ
    # ==========================================================================

    def construir_interfaz(self):

        # ----------------------------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------------------------

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        encabezado.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        titulo = ctk.CTkLabel(
            encabezado,
            text="⚡ EduControl",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color="#38bdf8"
        )

        titulo.pack(
            side="left"
        )

        subtitulo = ctk.CTkLabel(
            encabezado,
            text="Panel de Administración de Estudiantes",
            font=ctk.CTkFont(
                size=13
            ),
            text_color="#94a3b8"
        )

        subtitulo.pack(
            side="right",
            pady=8
        )

        # ----------------------------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # ----------------------------------------------------------------------

        contenido = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        contenido.grid_columnconfigure(
            0,
            weight=3
        )

        contenido.grid_columnconfigure(
            1,
            weight=2
        )

        contenido.grid_rowconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------------------------
        # PANEL IZQUIERDO
        # ----------------------------------------------------------------------

        panel_formulario = ctk.CTkFrame(
            contenido,
            corner_radius=14
        )

        panel_formulario.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # Título
        titulo_formulario = ctk.CTkLabel(
            panel_formulario,
            text="📝 Registro de Estudiante",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            text_color="#38bdf8"
        )

        titulo_formulario.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        # ----------------------------------------------------------------------
        # NOMBRE
        # ----------------------------------------------------------------------

        etiqueta_nombre = ctk.CTkLabel(
            panel_formulario,
            text="Nombre completo"
        )

        etiqueta_nombre.pack(
            anchor="w",
            padx=20,
            pady=(5, 3)
        )

        self.txt_nombre = ctk.CTkEntry(
            panel_formulario,
            placeholder_text="Nombre y apellido",
            height=38
        )

        self.txt_nombre.pack(
            fill="x",
            padx=20
        )

        # ----------------------------------------------------------------------
        # CI
        # ----------------------------------------------------------------------

        etiqueta_ci = ctk.CTkLabel(
            panel_formulario,
            text="C.I. / DNI"
        )

        etiqueta_ci.pack(
            anchor="w",
            padx=20,
            pady=(12, 3)
        )

        self.txt_ci = ctk.CTkEntry(
            panel_formulario,
            placeholder_text="Número de documento",
            height=38
        )

        self.txt_ci.pack(
            fill="x",
            padx=20
        )

        # ----------------------------------------------------------------------
        # CURSO
        # ----------------------------------------------------------------------

        etiqueta_curso = ctk.CTkLabel(
            panel_formulario,
            text="Nivel / Curso"
        )

        etiqueta_curso.pack(
            anchor="w",
            padx=20,
            pady=(12, 3)
        )

        self.cmb_curso = ctk.CTkComboBox(
            panel_formulario,
            values=[
                "1º Secundaria",
                "2º Secundaria",
                "3º Secundaria",
                "4º Secundaria",
                "5º Secundaria",
                "6º Secundaria"
            ],
            height=38
        )

        self.cmb_curso.pack(
            fill="x",
            padx=20
        )

        self.cmb_curso.set(
            "1º Secundaria"
        )

        # ----------------------------------------------------------------------
        # TURNO
        # ----------------------------------------------------------------------

        grupo_turno = ctk.CTkFrame(
            panel_formulario,
            fg_color="#172033",
            corner_radius=10
        )

        grupo_turno.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )

        etiqueta_turno = ctk.CTkLabel(
            grupo_turno,
            text="Turno Académico",
            font=ctk.CTkFont(
                weight="bold"
            ),
            text_color="#38bdf8"
        )

        etiqueta_turno.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        self.turno = ctk.StringVar(
            value="Mañana"
        )

        fila_turnos = ctk.CTkFrame(
            grupo_turno,
            fg_color="transparent"
        )

        fila_turnos.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        radio_manana = ctk.CTkRadioButton(
            fila_turnos,
            text="Mañana",
            variable=self.turno,
            value="Mañana"
        )

        radio_manana.pack(
            side="left",
            padx=10
        )

        radio_tarde = ctk.CTkRadioButton(
            fila_turnos,
            text="Tarde",
            variable=self.turno,
            value="Tarde"
        )

        radio_tarde.pack(
            side="left",
            padx=10
        )

        # ----------------------------------------------------------------------
        # ACTIVIDADES
        # ----------------------------------------------------------------------

        grupo_actividades = ctk.CTkFrame(
            panel_formulario,
            fg_color="#172033",
            corner_radius=10
        )

        grupo_actividades.pack(
            fill="x",
            padx=20,
            pady=5
        )

        etiqueta_actividades = ctk.CTkLabel(
            grupo_actividades,
            text="Actividades / Intereses",
            font=ctk.CTkFont(
                weight="bold"
            ),
            text_color="#38bdf8"
        )

        etiqueta_actividades.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=15,
            pady=(10, 5)
        )

        self.chk_deporte = ctk.CTkCheckBox(
            grupo_actividades,
            text="Deporte"
        )

        self.chk_deporte.grid(
            row=1,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.chk_musica = ctk.CTkCheckBox(
            grupo_actividades,
            text="Música"
        )

        self.chk_musica.grid(
            row=1,
            column=1,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.chk_ciencia = ctk.CTkCheckBox(
            grupo_actividades,
            text="Ciencia"
        )

        self.chk_ciencia.grid(
            row=2,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.chk_arte = ctk.CTkCheckBox(
            grupo_actividades,
            text="Arte"
        )

        self.chk_arte.grid(
            row=2,
            column=1,
            padx=15,
            pady=(5, 12),
            sticky="w"
        )

        # ----------------------------------------------------------------------
        # OBSERVACIONES
        # ----------------------------------------------------------------------

        etiqueta_observaciones = ctk.CTkLabel(
            panel_formulario,
            text="Observaciones"
        )

        etiqueta_observaciones.pack(
            anchor="w",
            padx=20,
            pady=(10, 3)
        )

        self.txt_obs = ctk.CTkTextbox(
            panel_formulario,
            height=75
        )

        self.txt_obs.pack(
            fill="x",
            padx=20
        )

        # ----------------------------------------------------------------------
        # BOTONES
        # ----------------------------------------------------------------------

        fila_botones = ctk.CTkFrame(
            panel_formulario,
            fg_color="transparent"
        )

        fila_botones.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.btn_guardar = ctk.CTkButton(
            fila_botones,
            text="Guardar",
            command=self.guardar_estudiante
        )

        self.btn_guardar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=3
        )

        self.btn_editar = ctk.CTkButton(
            fila_botones,
            text="Editar",
            command=self.cargar_para_editar,
            fg_color="#475569",
            hover_color="#334155"
        )

        self.btn_editar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=3
        )

        self.btn_eliminar = ctk.CTkButton(
            fila_botones,
            text="Eliminar",
            command=self.eliminar_estudiante,
            fg_color="#dc2626",
            hover_color="#b91c1c"
        )

        self.btn_eliminar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=3
        )

        self.btn_limpiar = ctk.CTkButton(
            fila_botones,
            text="Limpiar",
            command=self.limpiar_formulario,
            fg_color="#475569",
            hover_color="#334155"
        )

        self.btn_limpiar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=3
        )

        # ----------------------------------------------------------------------
        # PANEL DERECHO
        # ----------------------------------------------------------------------

        panel_lista = ctk.CTkFrame(
            contenido,
            corner_radius=14
        )

        panel_lista.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        titulo_lista = ctk.CTkLabel(
            panel_lista,
            text="👥 Estudiantes registrados",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            text_color="#38bdf8"
        )

        titulo_lista.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        # ----------------------------------------------------------------------
        # BÚSQUEDA
        # ----------------------------------------------------------------------

        self.txt_buscar = ctk.CTkEntry(
            panel_lista,
            placeholder_text="🔍 Buscar por nombre o CI...",
            height=40
        )

        self.txt_buscar.pack(
            fill="x",
            padx=20,
            pady=(0, 12)
        )

        self.txt_buscar.bind(
            "<KeyRelease>",
            self.refrescar_lista
        )

        # ----------------------------------------------------------------------
        # LISTA
        # ----------------------------------------------------------------------

        self.lista = ctk.CTkScrollableFrame(
            panel_lista,
            corner_radius=8
        )

        self.lista.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        # ----------------------------------------------------------------------
        # BOTÓN EXPEDIENTE
        # ----------------------------------------------------------------------

        self.btn_ver_ficha = ctk.CTkButton(
            panel_lista,
            text="📄 Abrir Expediente",
            command=self.abrir_ficha_completa,
            height=40
        )

        self.btn_ver_ficha.pack(
            fill="x",
            padx=20,
            pady=20
        )

    # ==========================================================================
    # CAPTURAR DATOS
    # ==========================================================================

    def capturar_datos(self):

        actividades = []

        if self.chk_deporte.get():
            actividades.append("Deporte")

        if self.chk_musica.get():
            actividades.append("Música")

        if self.chk_ciencia.get():
            actividades.append("Ciencia")

        if self.chk_arte.get():
            actividades.append("Arte")

        return {
            "nombre": self.txt_nombre.get().strip(),

            "ci": self.txt_ci.get().strip(),

            "curso": self.cmb_curso.get(),

            "turno": self.turno.get(),

            "actividades": ", ".join(
                actividades
            ),

            "observaciones": self.txt_obs.get(
                "1.0",
                "end"
            ).strip()
        }

    # ==========================================================================
    # VALIDACIÓN
    # ==========================================================================

    def es_valido(self, datos):

        if len(datos["nombre"]) < 3:

            messagebox.showwarning(
                "Validación",
                "El nombre ingresado es muy corto (mín. 3 letras)."
            )

            return False

        if not datos["ci"].isdigit():

            messagebox.showwarning(
                "Validación",
                "El campo CI debe contener únicamente dígitos numéricos."
            )

            return False

        return True

    # ==========================================================================
    # GUARDAR
    # ==========================================================================

    def guardar_estudiante(self):

        datos = self.capturar_datos()

        if not self.es_valido(datos):
            return

        # Editar
        if self.id_edicion is not None:

            self.expedientes[
                self.id_edicion
            ] = datos

            self.id_edicion = None

            messagebox.showinfo(
                "Éxito",
                "Expediente actualizado correctamente."
            )

        # Nuevo
        else:

            self.expedientes.append(
                datos
            )

            messagebox.showinfo(
                "Éxito",
                "Estudiante registrado satisfactoriamente."
            )

        self.refrescar_lista()

        self.limpiar_formulario()

    # ==========================================================================
    # REFRESCAR LISTA
    # ==========================================================================

    def refrescar_lista(self, event=None):

        filtro = self.txt_buscar.get().lower().strip()

        # Eliminar elementos anteriores
        for widget in self.lista.winfo_children():
            widget.destroy()

        for indice, estudiante in enumerate(
            self.expedientes
        ):

            nombre = estudiante["nombre"].lower()

            ci = estudiante["ci"].lower()

            if (
                filtro in nombre
                or filtro in ci
            ):

                self.crear_elemento_lista(
                    indice,
                    estudiante
                )

    # ==========================================================================
    # ELEMENTO DE LISTA
    # ==========================================================================

    def crear_elemento_lista(
        self,
        indice,
        estudiante
    ):

        tarjeta = ctk.CTkFrame(
            self.lista,
            corner_radius=8
        )

        tarjeta.pack(
            fill="x",
            pady=4
        )

        texto = (
            f"{estudiante['nombre']}\n"
            f"CI: {estudiante['ci']}  •  "
            f"{estudiante['curso']}"
        )

        etiqueta = ctk.CTkLabel(
            tarjeta,
            text=texto,
            justify="left",
            anchor="w"
        )

        etiqueta.pack(
            fill="x",
            padx=12,
            pady=10
        )

        # Guardar índice
        tarjeta.bind(
            "<Button-1>",
            lambda evento,
            i=indice:
            self.seleccionar_estudiante(i)
        )

        etiqueta.bind(
            "<Button-1>",
            lambda evento,
            i=indice:
            self.seleccionar_estudiante(i)
        )

        tarjeta.indice = indice

    # ==========================================================================
    # SELECCIÓN
    # ==========================================================================

    def seleccionar_estudiante(self, indice):

        self.indice_seleccionado = indice

        # Marcar visualmente
        for widget in self.lista.winfo_children():

            widget.configure(
                fg_color=("gray86", "gray17")
            )

        for widget in self.lista.winfo_children():

            if getattr(
                widget,
                "indice",
                None
            ) == indice:

                widget.configure(
                    fg_color="#075985"
                )

    # ==========================================================================
    # OBTENER SELECCIONADO
    # ==========================================================================

    def obtener_indice_seleccionado(self):

        if hasattr(
            self,
            "indice_seleccionado"
        ):

            indice = self.indice_seleccionado

            if (
                indice is not None
                and indice < len(self.expedientes)
            ):

                return indice

        return None

    # ==========================================================================
    # EDITAR
    # ==========================================================================

    def cargar_para_editar(self):

        indice = self.obtener_indice_seleccionado()

        if indice is None:

            messagebox.showwarning(
                "Atención",
                "Selecciona un estudiante de la lista."
            )

            return

        estudiante = self.expedientes[indice]

        self.txt_nombre.delete(
            0,
            "end"
        )

        self.txt_nombre.insert(
            0,
            estudiante["nombre"]
        )

        self.txt_ci.delete(
            0,
            "end"
        )

        self.txt_ci.insert(
            0,
            estudiante["ci"]
        )

        self.cmb_curso.set(
            estudiante["curso"]
        )

        self.turno.set(
            estudiante["turno"]
        )

        # Actividades
        self.chk_deporte.deselect()
        self.chk_musica.deselect()
        self.chk_ciencia.deselect()
        self.chk_arte.deselect()

        actividades = estudiante[
            "actividades"
        ]

        if "Deporte" in actividades:
            self.chk_deporte.select()

        if "Música" in actividades:
            self.chk_musica.select()

        if "Ciencia" in actividades:
            self.chk_ciencia.select()

        if "Arte" in actividades:
            self.chk_arte.select()

        # Observaciones
        self.txt_obs.delete(
            "1.0",
            "end"
        )

        self.txt_obs.insert(
            "1.0",
            estudiante["observaciones"]
        )

        self.id_edicion = indice

    # ==========================================================================
    # ELIMINAR
    # ==========================================================================

    def eliminar_estudiante(self):

        indice = self.obtener_indice_seleccionado()

        if indice is None:

            messagebox.showwarning(
                "Atención",
                "Selecciona un estudiante a eliminar."
            )

            return

        estudiante = self.expedientes[
            indice
        ]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            (
                "¿Estás seguro de eliminar este registro?\n\n"
                f"{estudiante['nombre']}"
            )
        )

        if confirmar:

            self.expedientes.pop(
                indice
            )

            self.indice_seleccionado = None

            self.refrescar_lista()

            self.limpiar_formulario()

    # ==========================================================================
    # LIMPIAR FORMULARIO
    # ==========================================================================

    def limpiar_formulario(self):

        self.txt_nombre.delete(
            0,
            "end"
        )

        self.txt_ci.delete(
            0,
            "end"
        )

        self.cmb_curso.set(
            "1º Secundaria"
        )

        self.turno.set(
            "Mañana"
        )

        self.chk_deporte.deselect()
        self.chk_musica.deselect()
        self.chk_ciencia.deselect()
        self.chk_arte.deselect()

        self.txt_obs.delete(
            "1.0",
            "end"
        )

        self.id_edicion = None

    # ==========================================================================
    # ABRIR EXPEDIENTE
    # ==========================================================================

    def abrir_ficha_completa(self):

        indice = self.obtener_indice_seleccionado()

        if indice is None:

            messagebox.showwarning(
                "Atención",
                "Selecciona un estudiante para consultar."
            )

            return

        datos = self.expedientes[
            indice
        ]

        FichaEstudiante(
            self,
            datos
        )


# ==============================================================================
# EJECUCIÓN
# ==============================================================================

if __name__ == "__main__":

    app = GestionEstudiantesApp()

    app.mainloop()