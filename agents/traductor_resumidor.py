# agents/traductor_resumidor.py

from google.cloud import translate_v2 as translate
from vertexai.preview.language_models import TextGenerationModel
import os
from vertexai import init
init(project="gen-lang-client-0241827889", location="europe-west4")

class TraductorResumidor:
    def __init__(self, idioma_objetivo='es'):
        self.idioma_objetivo = idioma_objetivo
        self.translate_client = translate.Client()
        self.modelo_gemini = TextGenerationModel.from_pretrained("text-bison")

    def traducir(self, texto):
        detectado = self.translate_client.detect_language(texto)
        if detectado['language'] != self.idioma_objetivo:
            traduccion = self.translate_client.translate(texto, target_language=self.idioma_objetivo)
            return traduccion['translatedText']
        return texto

    def resumir(self, texto):
        prompt = f"""Resume el siguiente texto de arte y cultura en 1 o 2 párrafos atractivos y claros. En español:

Texto:
\"\"\"
{texto}
\"\"\"

Resumen:"""
        respuesta = self.modelo_gemini.predict(
            prompt=prompt,
            temperature=0.4,
            max_output_tokens=300,
            top_p=0.8,
            top_k=40,
        )
        return respuesta.text.strip()

    def traducir_y_resumir(self, texto):
        traducido = self.traducir(texto)
        return self.resumir(traducido)
