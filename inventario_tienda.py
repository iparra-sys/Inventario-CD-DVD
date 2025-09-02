import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- BBDD -----------------
def conexion_bbdd():
    con = sqlite3.connect("media.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS MEDIA (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE TEXT,
            TIPO TEXT,
            GENERO TEXT,
            ESTADO TEXT
        )
    """)
    con.commit()
    con.close()

conexion_bbdd()

# ---------------- CRUD -----------------
def insertar():
    con = sqlite3.connect("media.db")
    cur = con.cursor()
    cur.execute("INSERT INTO MEDIA (NOMBRE, TIPO, GENERO, ESTADO) VALUES (?,?,?,?)",
                (nombre_var.get(), tipo_var.get(), genero_var.get(), estado_var.get()))
    con.commit()
    con.close()
    mostrar()
    limpiar()
    messagebox.showinfo("BBDD", "Registro agregado")

def mostrar():
    for i in tabla.get_children():
        tabla.delete(i)
    con = sqlite3.connect("media.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM MEDIA")
    for row in cur.fetchall():
        tabla.insert("", "end", values=row)
    con.close()

def eliminar():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccione un registro")
        return
    item = tabla.item(seleccionado)
    id = item["values"][0]
    con = sqlite3.connect("media.db")
    cur = con.cursor()
    cur.execute("DELETE FROM MEDIA WHERE ID=?", (id,))
    con.commit()
    con.close()
    mostrar()
    messagebox.showinfo("BBDD", "Registro eliminado")

def editar():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccione un registro")
        return
    item = tabla.item(seleccionado)
    id = item["values"][0]
    con = sqlite3.connect("media.db")
    cur = con.cursor()
    cur.execute("UPDATE MEDIA SET NOMBRE=?, TIPO=?, GENERO=?, ESTADO=? WHERE ID=?",
                (nombre_var.get(), tipo_var.get(), genero_var.get(), estado_var.get(), id))
    con.commit()
    con.close()
    mostrar()
    limpiar()
    messagebox.showinfo("BBDD", "Registro actualizado")

def buscar():
    for i in tabla.get_children():
        tabla.delete(i)
    con = sqlite3.connect("media.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM MEDIA WHERE NOMBRE LIKE ?", ('%'+buscar_var.get()+'%',))
    for row in cur.fetchall():
        tabla.insert("", "end", values=row)
    con.close()

def limpiar():
    nombre_var.set("")
    tipo_var.set("DVD")
    genero_var.set("")
    estado_var.set("Disponible")
    buscar_var.set("")

# ---------------- GUI -----------------
root = tk.Tk()
root.title("Gestión de CDs y Películas")
root.geometry("750x550")
root.configure(bg="#0A2647")  
root.iconbitmap("icono_cd.ico")


# --------- Variables -------------
nombre_var = tk.StringVar()
tipo_var = tk.StringVar(value="DVD")
genero_var = tk.StringVar()
estado_var = tk.StringVar(value="Disponible")
buscar_var = tk.StringVar()

# ----------- Estilos ------------
style = ttk.Style()
style.theme_use("clam")


style.configure("Treeview",
                background="#144272",  
                foreground="white",
                rowheight=25,
                fieldbackground="#144272")
style.configure("Treeview.Heading",
                background="#205295",  
                foreground="white",
                font=("Arial", 10, "bold"))

style.map("Treeview",
          background=[("selected", "#2C74B3")]) 

# ----------- Formulario ------------
frame_form = tk.Frame(root, bg="#0A2647", padx=10, pady=10)
frame_form.pack(fill="x")

tk.Label(frame_form, text="Nombre:", fg="white", bg="#0A2647").grid(row=0, column=0, sticky="e")
tk.Entry(frame_form, textvariable=nombre_var, bg="#205295", fg="white", insertbackground="white").grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Tipo CD:", fg="white", bg="#0A2647").grid(row=1, column=0, sticky="e")
tk.OptionMenu(frame_form, tipo_var, "DVD", "VCD").grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_form, text="Género:", fg="white", bg="#0A2647").grid(row=2, column=0, sticky="e")
tk.Entry(frame_form, textvariable=genero_var, bg="#205295", fg="white", insertbackground="white").grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Estado:", fg="white", bg="#0A2647").grid(row=3, column=0, sticky="e")
tk.OptionMenu(frame_form, estado_var, "Disponible", "Prestado").grid(row=3, column=1, padx=5, pady=5, sticky="w")

# ----------- Botones ------------
frame_btns = tk.Frame(root, pady=10, bg="#0A2647")
frame_btns.pack(fill="x")

tk.Button(frame_btns, text="Agregar", command=insertar, bg="#2C74B3", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_btns, text="Editar", command=editar, bg="#205295", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_btns, text="Eliminar", command=eliminar, bg="#144272", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame_btns, text="Limpiar", command=limpiar, bg="#0A2647", fg="white").grid(row=0, column=3, padx=5)

# ----------- Buscar ------------
frame_search = tk.Frame(root, pady=5, bg="#0A2647")
frame_search.pack(fill="x")
tk.Label(frame_search, text="Buscar por nombre:", fg="white", bg="#0A2647").grid(row=0, column=0, sticky="e")
tk.Entry(frame_search, textvariable=buscar_var, bg="#205295", fg="white", insertbackground="white").grid(row=0, column=1, padx=5)
tk.Button(frame_search, text="Buscar", command=buscar, bg="#2C74B3", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame_search, text="Mostrar todos", command=mostrar, bg="#144272", fg="white").grid(row=0, column=3, padx=5)

# ----------- Tabla ------------
frame_tabla = tk.Frame(root, bg="#0A2647")
frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Tipo", "Género", "Estado"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Tipo", text="Tipo CD")
tabla.heading("Género", text="Género")
tabla.heading("Estado", text="Estado")
tabla.pack(fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

mostrar()
root.mainloop()
