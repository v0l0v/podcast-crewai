# agents/generador_artista.py

import os
import csv
from datetime import date
import google.generativeai as genai
from dotenv import load_dotenv
from agents.artista_oculto import ArtistaOculto

class GeneradorArtista:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.historial_csv = "output/historial_artistas.csv"
        self._asegurar_historial()

    def _asegurar_historial(self):
        if not os.path.exists(self.historial_csv):
            with open(self.historial_csv, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["fecha", "artista"])

    def _registrar_artista(self, nombre):
        with open(self.historial_csv, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([str(date.today()), nombre])

    def _consultar_gemini(self, artista):
        prompt = f"""
Eres un experto en historia del arte. Quiero que interpretes al artista {artista}, sin decir su nombre, y generes lo siguiente:

1. Nueve pistas únicas sobre tu identidad. Habla en primera persona.
2. Una reflexión personal como artista oculto (filosófica o emotiva).
3. Una breve revelación con tu nombre: "Soy..."
4. Un consejo final inspirador para quien ama el arte.

Devuelve todo separado por etiquetas:
PISTAS:
- ...
- ...
REFLEXION:
...
RESOLUCION:
...
CONSEJO:
...
        """

        respuesta = self.model.generate_content(prompt)
        return respuesta.text

    def _parsear_respuesta(self, texto):
        secciones = {"PISTAS": [], "REFLEXION": "", "RESOLUCION": "", "CONSEJO": ""}
        actual = None
        for linea in texto.splitlines():
            linea = linea.strip()
            if linea.startswith("PISTAS"):
                actual = "PISTAS"
            elif linea.startswith("REFLEXION"):
                actual = "REFLEXION"
            elif linea.startswith("RESOLUCION"):
                actual = "RESOLUCION"
            elif linea.startswith("CONSEJO"):
                actual = "CONSEJO"
            elif actual == "PISTAS" and linea.startswith("-"):
                secciones["PISTAS"].append(linea.lstrip("- ").strip())
            elif actual and linea:
                secciones[actual] += " " + linea
        return secciones

    def generar_bloque_automatico(self):
        artista = input("🎭 ¿Quién será el artista oculto de hoy? ").strip()
        print(f"🔍 Buscando pistas para {artista}...\n")
        texto = self._consultar_gemini(artista)
        datos = self._parsear_respuesta(texto)

        # Montar audio con artista_oculto
        bloqueador = ArtistaOculto()
        ruta = bloqueador.generar_bloque(
            artista=artista,
            pistas=datos["PISTAS"],
            reflexion=datos["REFLEXION"],
            resolucion=datos["RESOLUCION"],
            consejo=datos["CONSEJO"]
        )

        self._registrar_artista(artista)
        return ruta
