# podcastgenerator.py

import subprocess
import threading
from tkinter import Tk, Button, Text, Scrollbar, END, RIGHT, LEFT, Y, BOTH, Frame, Label, Entry, StringVar

# Variables globales para pasar al ensamblador (como archivo temporal)
CONFIG_PATH = "output/config_usuario.txt"

def ejecutar_ensamblador(log_widget, noticias_var, artista_var):
    def run():
        log_widget.insert(END, "\n🛠️ Ensamblando el podcast final...\n")
        log_widget.see(END)

        # Guardar config temporal
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(f"noticias={noticias_var.get()}\n")
            f.write(f"artista={artista_var.get().strip()}\n")

        try:
            subprocess.run(["python", "ensamblador.py"], check=True)
            log_widget.insert(END, "✅ ¡Podcast ensamblado con éxito!\n")
        except subprocess.CalledProcessError as e:
            log_widget.insert(END, f"❌ Error: {e}\n")
        log_widget.see(END)

    threading.Thread(target=run).start()

def crear_interfaz():
    root = Tk()
    root.title("🎙️ Generador de Podcast de Arte")
    root.geometry("720x460")

    # Frame para scroll y logs
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    salida_texto = Text(frame, wrap='word', yscrollcommand=scrollbar.set, height=12)
    salida_texto.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=salida_texto.yview)

    # Entradas de configuración
    noticias_var = StringVar(value="3")
    artista_var = StringVar(value="")

    Label(root, text="Número de noticias:").pack()
    Entry(root, textvariable=noticias_var, width=5, justify='center').pack()

    Label(root, text="Nombre del artista oculto:").pack()
    Entry(root, textvariable=artista_var, width=30).pack()

    # Botón
    Button(root, text="🎧 Ensamblar Podcast Final", bg="#d4f4dd", font=('Arial', 14),
           command=lambda: ejecutar_ensamblador(salida_texto, noticias_var, artista_var)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()
