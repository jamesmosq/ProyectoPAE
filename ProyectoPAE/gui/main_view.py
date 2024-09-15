import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Estudiante
from storage.estudiante_dao import EstudianteDAO
from .barcode_view import BarcodeView

class MainView(tk.Tk):
    def __init__(self, estudiante_dao, estudiante_action_dao):
        super().__init__()
        self.estudiante_dao = estudiante_dao
        self.estudiante_action_dao = estudiante_action_dao
        self.title("Datos Estudiantes")
        self.geometry("1000x800")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        info_frame = tk.LabelFrame(main_frame, text="Información del Estudiante", padx=10, pady=10)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.fields = ['Documento', 'Nombres', 'Apellidos', 'Grado']
        self.entries = {}

        for i, field in enumerate(self.fields):
            ttk.Label(info_frame, text=field).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(info_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[field] = entry

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Buscar", command=self.search_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insertar", command=self.insert_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.update_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Borrar", command=self.delete_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Mostrar Todos", command=self.show_all_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Escanear Código", command=self.open_barcode_view).pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=self.fields, show="headings")
        for field in self.fields:
            self.tree.heading(field, text=field)
        self.tree.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def search_estudiante(self):
        documento = self.entries['Documento'].get()
        if not documento:
            messagebox.showwarning("Advertencia", "Por favor, ingrese Documento de estudiante")
            return

        estudiante = self.estudiante_dao.buscar_estudiante(documento)
        if estudiante:
            self.display_estudiante(estudiante)
        else:
            messagebox.showinfo("Información", "No se encontró el estudiante")

    def insert_estudiante(self):
        values = [self.entries[field].get() for field in self.fields]
        estudiante = Estudiante(*values)
        if self.estudiante_dao.crear_estudiante(estudiante):
            messagebox.showinfo("Éxito", "Estudiante insertado correctamente")
            self.clear_fields()
            self.show_all_estudiante()

    def update_estudiante(self):
        values = [self.entries[field].get() for field in self.fields]
        estudiante = Estudiante(*values)
        if self.estudiante_dao.actualizar_estudiante(estudiante):
            messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
            self.show_all_estudiante()

    def delete_estudiante(self):
        documento = self.entries['Documento'].get()
        if not documento:
            messagebox.showwarning("Advertencia", "Por favor, ingrese Documento de estudiante")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este estudiante?"):
            if self.estudiante_dao.eliminar_estudiante(documento):
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
                self.clear_fields()
                self.show_all_estudiante()

    def show_all_estudiante(self):
        estudiantes = self.estudiante_dao.ver_estudiantes()
        self.display_estudiantes(estudiantes)

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def display_estudiante(self, estudiante):
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=(estudiante.documento, estudiante.nombres, estudiante.apellidos, estudiante.grado))

    def display_estudiantes(self, estudiantes):
        self.tree.delete(*self.tree.get_children())
        for estudiante in estudiantes:
            self.tree.insert("", "end", values=(estudiante.documento, estudiante.nombres, estudiante.apellidos, estudiante.grado))

    def open_barcode_view(self):
        barcode_window = tk.Toplevel(self)
        barcode_app = BarcodeView(self.estudiante_action_dao, master=barcode_window)
        barcode_app.pack(fill=tk.BOTH, expand=True)