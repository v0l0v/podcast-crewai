def ejecutar_ensamblador():
    def run():
        salida_texto.insert(END, "\n🛠️ Ensamblando el podcast final...\n")
        try:
            subprocess.run(["python", "ensamblador.py"], check=True)
            salida_texto.insert(END, "✅ ¡Podcast ensamblado con éxito!\n")
        except subprocess.CalledProcessError as e:
            salida_texto.insert(END, f"❌ Error: {e}\n")

    threading.Thread(target=run).start()
