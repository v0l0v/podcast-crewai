# agents/locutor.py

import os
from google.cloud import texttospeech
from pydub import AudioSegment
from io import BytesIO

class Locutor:
    def __init__(self, voz="es-ES-Wavenet-D"):
        self.voz = voz

        # Inicializar cliente de Google TTS
        self.tts_client = texttospeech.TextToSpeechClient.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )

    def texto_a_audio(self, texto, nombre_archivo):
        """Convierte texto a archivo MP3 usando Google TTS"""
        input_text = texttospeech.SynthesisInput(text=texto)

        voice_params = texttospeech.VoiceSelectionParams(
            language_code="es-ES",
            name=self.voz,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0
        )

        try:
            response = self.tts_client.synthesize_speech(
                input=input_text,
                voice=voice_params,
                audio_config=audio_config
            )

            ruta_salida = f"output/{nombre_archivo}.mp3"
            with open(ruta_salida, "wb") as out:
                out.write(response.audio_content)
            print(f"✅ Audio guardado en {ruta_salida}")
            return ruta_salida

        except Exception as e:
            print(f"❌ Error al generar audio: {e}")
            return None

    def texto_a_segmento(self, texto):
        """Devuelve un objeto AudioSegment (útil para combinaciones)"""
        input_text = texttospeech.SynthesisInput(text=texto)

        voice_params = texttospeech.VoiceSelectionParams(
            language_code="es-ES",
            name=self.voz,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
