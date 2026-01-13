import tkinter as tk
from tkinter import ttk
from pathlib import Path
import threading
import entorno

APP_DIR = Path(__file__).resolve().parent
BACKGROUND = APP_DIR / "fondo.png"

current_thread = None

def set_buttons_state(state: str):
    for b in btn_widgets:
        b.configure(state=state)

def run_entorno(n: int):
    global current_thread

    # Si ya hay una sesion corriendo, no lanzar otra
    if current_thread is not None and current_thread.is_alive():
        return

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    set_buttons_state("disabled")

    def worker():
        try:
            entorno.main(n, screen_w, screen_h)
        finally:
            # Rehabilitar botones en el hilo principal de Tk [web:256]
            root.after(0, lambda: set_buttons_state("normal"))

    current_thread = threading.Thread(target=worker)  # no daemon: termina bien
    current_thread.start()

root = tk.Tk()
root.title("Nexe Entorno")
root.geometry("420x260")
root.resizable(False, False)

bg_img = tk.PhotoImage(file=str(BACKGROUND))
bg_label = tk.Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frm = ttk.Frame(root, padding=14)
frm.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(frm, text="Selecciona cuantas imagenes:", font=("Segoe UI", 13)).grid(
    row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
)

btn_widgets = []
for i, (txt, n) in enumerate([("2 imagenes", 2), ("4 imagenes", 4), ("6 imagenes", 6), ("8 imagenes", 8)]):
    r, c = divmod(i, 2)
    b = ttk.Button(frm, text=txt, command=lambda n=n: run_entorno(n))
    b.grid(row=1 + r, column=c, padx=8, pady=8, sticky="nsew")
    btn_widgets.append(b)

frm.columnconfigure(0, weight=1)
frm.columnconfigure(1, weight=1)

ttk.Label(frm, text="ESC para salir del entorno (ventana OpenCV).").grid(
    row=3, column=0, columnspan=2, sticky="w", pady=(10, 0)
)
ttk.Button(frm, text="Salir", command=root.destroy).grid(row=4, column=1, sticky="e", pady=(10, 0))

root.mainloop()
