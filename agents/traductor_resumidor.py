# agents/traductor_resumidor.py

import os
from google.cloud import translate_v2 as translate
from vertexai.language_models import TextGenerationModel
from vertexai import init

class TraductorResumidor:
    def __init__(self, idioma_objetivo='es'):
        self.idioma_objetivo = idioma_objetivo

        # Inicializa Vertex AI con el proyecto y región especificados en .env
        init(
            project=os.getenv("GOOGLE_PROJECT_ID"),
            location="us-central1"
        )

        # Cliente para traducción automática de Google
        self.translate_client = translate.Client()

        # Modelo de resumen de Vertex AI
        self.modelo_vertex = TextGenerationModel.from_pretrained("text-bison@001")

    def traducir(self, texto):
        """Traduce el texto si no está en el idioma objetivo"""
        detectado = self.translate_client.detect_language(texto)
        if detectado['language'] != self.idioma_objetivo:
            traduccion = self.translate_client.translate(
                texto,
                target_language=self.idioma_objetivo
            )
            return traduccion['translatedText']
        return texto

    def resumir(self, texto):
        """Genera un resumen conciso y atractivo del texto"""
        prompt = f"""
Resume el siguiente texto de arte y cultura en 1 o 2 párrafos atractivos y claros:

Texto:
\"\"\"
{texto}
\"\"\"

Resumen:
"""
        respuesta = self.modelo_vertex.predict(
            prompt,
            max_output_tokens=250
        )
        return respuesta.text.strip()

    def traducir_y_resumir(self, texto):
        """Pipeline completo: traducir si hace falta y luego resumir"""
        traducido = self.traducir(texto)
        return self.resumir(traducido)
