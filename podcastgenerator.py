# podcastgenerator.py

import subprocess
import threading
from tkinter import Tk, Button, Text, Scrollbar, END, RIGHT, LEFT, Y, BOTH, Frame

def ejecutar_ensamblador(log_widget):
    def run():
        log_widget.insert(END, "\n🛠️ Ensamblando el podcast final...\n")
        log_widget.see(END)
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
    root.geometry("700x400")

    # Frame para scroll
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)

    # Área de texto con scroll
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    salida_texto = Text(frame, wrap='word', yscrollcommand=scrollbar.set)
    salida_texto.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=salida_texto.yview)

    # Botón
    boton = Button(root, text="🎧 Ensamblar Podcast Final", bg="#d4f4dd",
                   font=('Arial', 14), command=lambda: ejecutar_ensamblador(salida_texto))
    boton.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()
