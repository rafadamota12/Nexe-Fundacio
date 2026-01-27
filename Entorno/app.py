# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
import json
import entorno

APP_DIR = Path(__file__).resolve().parent
BACKGROUND = APP_DIR / "logo.png"
DIR_ALUMNES = APP_DIR / "Alumnes"

current_thread = None
btn_widgets = []

# ----------------- Utilidades UI -----------------
def set_buttons_state(state: str):
    for b in btn_widgets:
        try:
            b.configure(state=state)
        except Exception:
            pass

def listar_alumnos(base: Path) -> list[str]:
    if not base.exists():
        return []
    return sorted([p.name for p in base.iterdir() if p.is_dir()])

# ----------------- Datos alumno -----------------
def obtener_stems_disponibles(alumno_dir: Path) -> list[str]:
    dir_audios = alumno_dir / "Audios"
    dir_imagenes = alumno_dir / "Imagenes"
    if not dir_audios.exists() or not dir_imagenes.exists():
        return []

    ext_img = {".jpg", ".jpeg", ".png"}
    ext_aud = {".mp3", ".wav", ".ogg"}

    imgs = {p.stem for p in dir_imagenes.iterdir() if p.is_file() and p.suffix.lower() in ext_img}
    auds = {p.stem for p in dir_audios.iterdir() if p.is_file() and p.suffix.lower() in ext_aud}
    return sorted(imgs & auds)

def favoritos_path(alumno_dir: Path) -> Path:
    return alumno_dir / "favoritos.json"

def leer_favoritos(alumno_dir: Path) -> list[str] | None:
    fp = favoritos_path(alumno_dir)
    if not fp.exists():
        return None
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
        favs = data.get("favoritos", None)
        if isinstance(favs, list):
            return [str(x) for x in favs]
    except Exception:
        return None
    return None

def escribir_favoritos(alumno_dir: Path, alumno: str, favoritos: list[str]):
    fp = favoritos_path(alumno_dir)
    payload = {"alumno": alumno, "favoritos": favoritos}
    fp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

def validar_par(seleccion: list[str]) -> bool:
    # Obligatorio número par
    return (len(seleccion) % 2) == 0

# ----------------- Lanzar entorno -----------------
def lanzar_entorno(alumno_dir: Path, stems: list[str] | None):
    global current_thread
    if current_thread is not None and current_thread.is_alive():
        return

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    set_buttons_state("disabled")

    def worker():
        try:
            entorno.main(alumno_dir, screen_w, screen_h, stems_favoritos=stems)
        except Exception as e:
            # Congelar el mensaje en el lambda para evitar NameError
            root.after(0, lambda msg=str(e): messagebox.showerror("Error", msg))
        finally:
            root.after(0, lambda: set_buttons_state("normal"))

    current_thread = threading.Thread(target=worker)
    current_thread.start()

# ----------------- Acciones -----------------
def iniciar_normal(alumno: str):
    if not alumno:
        messagebox.showwarning("Falta alumno", "Selecciona un alumno/a primero.")
        return

    alumno_dir = DIR_ALUMNES / alumno
    disponibles = obtener_stems_disponibles(alumno_dir)
    if not disponibles:
        messagebox.showerror("Sin contenido", f"No se encontraron pares en:\n{alumno_dir}/Imagenes y {alumno_dir}/Audios")
        return

    favs = leer_favoritos(alumno_dir)

    # Modo normal: no modificar JSON nunca.
    if favs is None:
        stems = disponibles
    else:
        stems = [s for s in disponibles if s in set(favs)]

    if not stems:
        messagebox.showerror("Sin favoritos", "favoritos.json existe pero no coincide con archivos actuales.")
        return

    # Forzar par también en modo normal
    if not validar_par(stems):
        messagebox.showwarning("Numero invalido", "Los favoritos deben ser un numero PAR (2, 4, 6, ...). Revisa 'Editar favoritos (tutor)'.")
        return

    lanzar_entorno(alumno_dir, stems)

def abrir_editor_tutor(alumno: str):
    if not alumno:
        messagebox.showwarning("Falta alumno", "Selecciona un alumno/a primero.")
        return

    alumno_dir = DIR_ALUMNES / alumno
    disponibles = obtener_stems_disponibles(alumno_dir)
    if not disponibles:
        messagebox.showerror("Sin contenido", f"No se encontraron pares en:\n{alumno_dir}/Imagenes y {alumno_dir}/Audios")
        return

    favs_prev = set(leer_favoritos(alumno_dir) or [])

    win = tk.Toplevel(root)
    win.title(f"Editar favoritos (tutor): {alumno}")
    win.geometry("560x560")
    win.resizable(False, False)

    tk.Label(
        win,
        text="Marca (si/no) que audios seran favoritas (debe ser numero PAR):",
        font=("Segoe UI", 14)
    ).pack(anchor="w", padx=12, pady=(12, 8))

    # --- Scrollable ---
    container = tk.Frame(win)
    container.pack(fill="both", expand=True, padx=12, pady=8)

    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    vars_por_stem: dict[str, tk.BooleanVar] = {}

    # --- Opción B: tk.Checkbutton grande ---
    for stem in disponibles:
        v = tk.BooleanVar(value=(stem in favs_prev))  # estado True/False 
        vars_por_stem[stem] = v

        cb = tk.Checkbutton(
            scroll_frame,
            text=stem,
            variable=v,                
            font=("Segoe UI", 18),      
            padx=20, pady=8,            
            anchor="w",
            justify="left"
        )
        cb.pack(anchor="w", fill="x")

    bottom = tk.Frame(win)
    bottom.pack(fill="x", padx=12, pady=(8, 12))

    def obtener_seleccion() -> list[str]:
        return [stem for stem, v in vars_por_stem.items() if v.get()]  # get True/False 

    def seleccionar_todo():
        for v in vars_por_stem.values():
            v.set(True)

    def limpiar():
        for v in vars_por_stem.values():
            v.set(False)

    def validar_y_alertar(seleccion: list[str]) -> bool:
        if not seleccion:
            messagebox.showwarning("Vacio", "Selecciona al menos 2 favorito.")
            return False
        if not validar_par(seleccion):
            messagebox.showwarning("Numero invalido", "Debes seleccionar un numero PAR de audios (2, 4, 6, ...).")
            return False
        return True

    def guardar():
        seleccion = obtener_seleccion()
        if not validar_y_alertar(seleccion):
            return
        escribir_favoritos(alumno_dir, alumno, seleccion)
        messagebox.showinfo("Guardado", f"Favoritos guardados en:\n{favoritos_path(alumno_dir)}")
        win.destroy()

    def guardar_e_iniciar():
        seleccion = obtener_seleccion()
        if not validar_y_alertar(seleccion):
            return
        escribir_favoritos(alumno_dir, alumno, seleccion)
        win.destroy()
        lanzar_entorno(alumno_dir, seleccion)

    # Botones
    ttk.Button(bottom, text="Seleccionar todo", command=seleccionar_todo).pack(side="left")
    ttk.Button(bottom, text="Limpiar", command=limpiar).pack(side="left", padx=8)
    ttk.Button(bottom, text="Guardar", command=guardar).pack(side="right")
    ttk.Button(bottom, text="Guardar e iniciar", command=guardar_e_iniciar).pack(side="right", padx=8)

# ----------------- UI principal -----------------
root = tk.Tk()
root.title("Nexe Entorno")
root.geometry("420x260")
root.resizable(False, False)

main_canvas = tk.Canvas(root, highlightthickness=0, bd=3)
main_canvas.pack(fill="both", expand=True)

bg_img = tk.PhotoImage(file=str(BACKGROUND))
main_canvas.create_image(0, 0, image=bg_img, anchor="nw")

title_lbl = tk.Label(main_canvas, text="Selecciona alumno/a:", font=("Segoe UI", 13), fg="#000000")
info_lbl = tk.Label(main_canvas, text="ESC para salir del entorno.", font=("Segoe UI", 10), bg="#ffffff", fg="#000000")

alumnos = listar_alumnos(DIR_ALUMNES)
alumno_var = tk.StringVar(value=alumnos[0] if alumnos else "")
combo_alumno = ttk.Combobox(main_canvas, textvariable=alumno_var, values=alumnos, state="readonly")

btn_iniciar = ttk.Button(main_canvas, text="Iniciar", command=lambda: iniciar_normal(alumno_var.get()))
btn_editar = ttk.Button(main_canvas, text="Editar favoritos (tutor)", command=lambda: abrir_editor_tutor(alumno_var.get()))
btn_exit = ttk.Button(main_canvas, text="Salir", command=root.destroy)

btn_widgets = [combo_alumno, btn_iniciar, btn_editar, btn_exit]

main_canvas.create_window(20, 20, anchor="nw", window=title_lbl)
main_canvas.create_window(70, 70, anchor="nw", window=combo_alumno, width=280, height=30)
main_canvas.create_window(70, 115, anchor="nw", window=btn_iniciar, width=140, height=32)
main_canvas.create_window(220, 115, anchor="nw", window=btn_editar, width=170, height=32)

main_canvas.create_window(20, 175, anchor="nw", window=info_lbl)
main_canvas.create_window(320, 210, anchor="nw", window=btn_exit, width=80, height=30)

if not alumnos:
    messagebox.showwarning(
        "Sin alumnos",
        f"No se encontraron carpetas en:\n{DIR_ALUMNES}\n\nCrea Alumnes/<Nombre>/Imagenes y Alumnes/<Nombre>/Audios."
    )

root.mainloop()
