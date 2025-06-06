# agents/locutor.py

import os
from google.cloud import texttospeech
from pydub import AudioSegment
from io import BytesIO

class Locutor:
    def __init__(self, voz="es-ES-Wavenet-D"):
        self.voz = voz
        self.tts_client = texttospeech.TextToSpeechClient.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )

    def _generar_parametros_voz(self):
        """Detecta automáticamente si la voz es masculina o femenina"""
        genero = (
            texttospeech.SsmlVoiceGender.MALE
            if "-A" in self.voz or "-B" in self.voz
            else texttospeech.SsmlVoiceGender.FEMALE
        )

        return texttospeech.VoiceSelectionParams(
            language_code="es-ES",
            name=self.voz,
            ssml_gender=genero
        )

    def texto_a_audio(self, texto, nombre_archivo):
        """Convierte texto a archivo MP3 usando Google TTS"""
        input_text = texttospeech.SynthesisInput(text=texto)
        voice_params = self._generar_parametros_voz()
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
        """Devuelve un objeto AudioSegment para combinación en el podcast"""
        input_text = texttospeech.SynthesisInput(text=texto)
        voice_params = self._generar_parametros_voz()
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        try:
            response = self.tts_client.synthesize_speech(
                input=input_text,
                voice=voice_params,
                audio_config=audio_config
            )

            return AudioSegment.from_file(BytesIO(response.audio_content), format="mp3")

        except Exception as e:
            print(f"❌ Error al generar segmento: {e}")
            return AudioSegment.silent(duration=1000)
