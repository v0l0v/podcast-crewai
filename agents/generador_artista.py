# agents/generador_artista.py

from vertexai import init
init(project="gen-lang-client-0241827889", location="europe-west4")
from vertexai.preview.language_models import TextGenerationModel
from agents.locutor import Locutor
from pydub import AudioSegment
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(prompt)


class GeneradorArtista:
    def __init__(self):
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path or not os.path.exists(cred_path):
            raise EnvironmentError("❌ Credencial JSON de Google Cloud no encontrada o mal configurada. Verifica GOOGLE_APPLICATION_CREDENTIALS.")
        else:
            print(f"🔐 Credencial detectada: {cred_path}")

        try:
            self.model = TextGenerationModel.from_pretrained("text-bison")
        except Exception as e:
            print("❌ No se pudo cargar el modelo Gemini 1.5 Pro:", e)
            self.model = None

        self.locutor_atenea = Locutor("es-ES-Wavenet-D")
        self.locutor_personaje = Locutor("es-ES-Wavenet-A")
        self.sonido_espera = "assets/espera_personaje.mp3"
        os.makedirs("output", exist_ok=True)

    def _consultar_gemini(self, nombre_artista):
        if not self.model:
            raise RuntimeError("Modelo Gemini no disponible. Verifica tu entorno y credenciales.")

        prompt = f"""
Eres un artista oculto. Te propongo el siguiente nombre: "{nombre_artista}".

1. Escribe 9 pistas que describan su estilo, logros o historia, sin mencionar su nombre.
2. Luego, crea una reflexión profunda del artista como si fuera él mismo.
3. Después, incluye una revelación donde diga quién es.
4. Por último, da un consejo o frase inspiradora para futuros artistas.

Usa este formato con doble salto entre secciones:
PISTAS:
(pista 1 a 9 numeradas)
REFLEXIÓN:
(texto)
RESOLUCIÓN:
(nombre revelado)
CONSEJO:
(texto motivador)
"""
        respuesta = self.model.predict(prompt, max_output_tokens=1000)
        return respuesta.text

    def generar_bloque_automatico(self):
        artista = input("🎨 ¿Qué artista quieres usar hoy como oculto?: ").strip()
        texto = self._consultar_gemini(artista)

        secciones = self._parsear_respuesta(texto)

        from agents.artista_oculto import ArtistaOculto
        bloqueador = ArtistaOculto()
        ruta, contenido = bloqueador.generar_bloque(
            artista=artista,
            pistas=secciones['pistas'],
            reflexion=secciones['reflexion'],
            resolucion=secciones['resolucion'],
            consejo=secciones['consejo']
        )
        return ruta, contenido

    def _parsear_respuesta(self, texto):
        bloques = {
            "pistas": [],
            "reflexion": "",
            "resolucion": "",
            "consejo": ""
        }
        partes = texto.split("PISTAS:")[-1].split("REFLEXIÓN:")
        if len(partes) >= 2:
            pistas_brutas = partes[0].strip().split("\n")
            bloques["pistas"] = [p.strip("-•1234567890. ").strip() for p in pistas_brutas if p.strip()]
            partes_restantes = partes[1].split("RESOLUCIÓN:")
            if len(partes_restantes) >= 2:
                bloques["reflexion"] = partes_restantes[0].strip()
                partes_finales = partes_restantes[1].split("CONSEJO:")
                if len(partes_finales) >= 2:
                    bloques["resolucion"] = partes_finales[0].strip()
                    bloques["consejo"] = partes_finales[1].strip()
        return bloques