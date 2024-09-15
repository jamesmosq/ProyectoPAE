import tkinter as tk
from tkinter import ttk, messagebox

class BarcodeView(ttk.Frame):
    def __init__(self, estudiante_action_dao, master=None):
        super().__init__(master)
        self.estudiante_action_dao = estudiante_action_dao
        self.master.title("Lectura con Código de Barras")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        barcode_frame = tk.LabelFrame(main_frame, text="Escanear Código de Barras", padx=10, pady=10)
        barcode_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.barcode_entry = ttk.Entry(barcode_frame, width=40)
        self.barcode_entry.grid(row=0, column=0, padx=5, pady=5)
        self.barcode_entry.bind("<Return>", self.handle_barcode_scan)

        tree_frame = tk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Documento", "Nombres", "Apellidos", "Grado", "Acción", "Fecha"),
                                 show="headings")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Grado", text="Grado")
        self.tree.heading("Acción", text="Acción")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def handle_barcode_scan(self, event):
        barcode = self.barcode_entry.get()
        if not barcode.isdigit():
            messagebox.showwarning("Advertencia", "El código de barras debe ser numérico")
            return

        action = self.estudiante_action_dao.registrar_accion(barcode)
        if action:
            self.display_action(action)
        else:
            messagebox.showinfo("Información", "No se encontraron resultados para este código")

        self.barcode_entry.delete(0, tk.END)

    def display_action(self, action):
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=(action.documento, action.nombres, action.apellidos,
                                            action.grado, action.action, action.consult_date))