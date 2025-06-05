# tools/transiciones.py

import os
import random
from pydub import AudioSegment

class Transiciones:
    def __init__(self, carpeta_sonidos="assets"):
        self.carpeta = carpeta_sonidos
        self.efectos = [os.path.join(self.carpeta, f)
                        for f in os.listdir(self.carpeta)
                        if f.endswith(".mp3")]

    def obtener_efecto(self):
        if not self.efectos:
            return AudioSegment.silent(duration=500)
        sonido = random.choice(self.efectos)
        return AudioSegment.from_file(sonido, format="mp3")
