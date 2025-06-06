# ensamblador.py

import os
from datetime import datetime
from pydub import AudioSegment
from glob import glob
from agents.locutor import Locutor
from agents.generador_artista import GeneradorArtista

CONFIG_PATH = "output/config_usuario.txt"

def cargar_config_usuario(ruta=CONFIG_PATH):
    config = {"noticias": 3, "artista": ""}
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                if "=" in linea:
                    clave, valor = linea.strip().split("=", 1)
                    if clave == "noticias":
                        try:
                            config["noticias"] = int(valor)
                        except:
                            pass
                    elif clave == "artista":
                        config["artista"] = valor.strip()
    return config

def ensamblar_podcast():
    os.makedirs("output", exist_ok=True)

    config = cargar_config_usuario()
    num_noticias = config["noticias"]
    nombre_artista = config["artista"]

    final = AudioSegment.silent(duration=500)
    atenea = Locutor("es-ES-Wavenet-D")
    texto_intro = "Bienvenidas y bienvenidos al podcast de arte diario. Soy Atenea, tu guía."
    final += atenea.texto_a_segmento(texto_intro)

    markdown = f"# 🎨 Podcast del {datetime.now().strftime('%d/%m/%Y')}\n\n"
    markdown += "## Introducción\n" + texto_intro.strip() + "\n\n"

    # 2. Noticias
    noticias = sorted(glob("output/noticia_*.mp3"))[:num_noticias]
    markdown += "## 📰 Noticias de Arte\n"
    for i, ruta in enumerate(noticias, 1):
        final += AudioSegment.from_file(ruta) + AudioSegment.silent(duration=500)
        try:
            with open(ruta.replace(".mp3", ".txt"), "r", encoding="utf-8") as f:
                resumen = f.read().strip()
        except:
            resumen = "Resumen no disponible."
        markdown += f"**Noticia {i}**:\n> {resumen}\n\n"

    # 3. Transición hacia el artista oculto
    transicion = "Ahora... presta atención. Llega nuestro invitado misterioso."
    final += atenea.texto_a_segmento(transicion)
    markdown += "\n## 🎭 El Artista Oculto\n"
    markdown += f"_Presentado por Atenea. Artista elegido: **{nombre_artista}**_\n\n"

    # 4. Bloque del artista oculto
    oculto = GeneradorArtista()
    ruta_oculto, texto_oculto = oculto.generar_bloque_automatico(nombre_artista)
    final += AudioSegment.from_file(ruta_oculto)

    markdown += "### Pistas:\n"
    for i, pista in enumerate(texto_oculto["pistas"], 1):
        markdown += f"- {pista}\n"
    markdown += "\n### Reflexión:\n" + texto_oculto["reflexion"] + "\n"
    markdown += "\n### Resolución:\n" + texto_oculto["resolucion"] + "\n"
    markdown += "\n### Consejo:\n" + texto_oculto["consejo"] + "\n"

    # 5. Despedida
    despedida = """
Gracias por acompañarnos. Puedes contarnos tu respuesta en barcolavadero.ovh. 
Mañana, nuevas pistas, nuevos artistas. ¡Hasta pronto!
    """
    final += atenea.texto_a_segmento(despedida)
    markdown += "\n## 👋 Despedida\n" + despedida.strip()

    # 6. Guardar archivos
    ahora = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"output/podcast_output_{ahora}"

    final.export(base + ".mp3", format="mp3")
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(markdown)

    html = markdown.replace("\n", "<br>").replace("**", "<b>").replace("#", "").replace("> ", "<i>").replace("_", "")
    with open(base + ".html", "w", encoding="utf-8") as f:
        f.write(f"<html><body>{html}</body></html>")

    print(f"\n✅ Podcast ensamblado: {base}.mp3")
    print(f"📝 Texto en Markdown: {base}.md")
    print(f"🌐 Versión HTML: {base}.html")

if __name__ == "__main__":
    ensamblar_podcast()
