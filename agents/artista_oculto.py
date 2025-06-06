# agents/artista_oculto.py

from agents.locutor import Locutor
from pydub import AudioSegment
import os

class ArtistaOculto:
    def __init__(self):
        self.atenea = Locutor("es-ES-Wavenet-D")
        self.personaje = Locutor("es-ES-Wavenet-A")
        self.musica_espera = "assets/espera_personaje.mp3"
        os.makedirs("output", exist_ok=True)

    def generar_bloque(self, artista, pistas, reflexion, resolucion, consejo):
        segmentos = []

        # Texto usado para versión escrita
        texto_total = {
            "artista": artista,
            "pistas": pistas,
            "reflexion": reflexion.strip(),
            "resolucion": resolucion.strip(),
            "consejo": consejo.strip()
        }

        # 1. Intro de Atenea
        intro = f"""
Ahora comenzamos una sección muy especial... <break time="400ms"/>
<emphasis level="moderate">El artista oculto</emphasis>.
Nuestro invitado misterioso nos dará pistas sobre su identidad.
¿Te atreves a adivinar quién es?
        """
        segmentos.append(self.atenea.texto_a_segmento(intro))

        # 2. Presentación del personaje
        intro_pj = "Hola. Soy un artista con una larga trayectoria... pero pocos me conocen por mi nombre. Escucha con atención..."
        segmentos.append(self.personaje.texto_a_segmento(intro_pj))

        # 3. Pistas
        for i, pista in enumerate(pistas, 1):
            texto_pista = f"Pista {i}: {pista}"
            segmentos.append(self.personaje.texto_a_segmento(texto_pista))

        # 4. Reflexión
        segmentos.append(self.personaje.texto_a_segmento(reflexion))

        # 5. Música de espera
        if os.path.exists(self.musica_espera):
            espera = AudioSegment.from_file(self.musica_espera)
            segmentos.append(espera[:30000])
        else:
            segmentos.append(AudioSegment.silent(duration=30000))

        # 6. Resolución
        segmentos.append(self.personaje.texto_a_segmento(resolucion))

        # 7. Consejo
        segmentos.append(self.personaje.texto_a_segmento(consejo))

        # 8. Cierre de Atenea
        cierre = "¿Lo habías adivinado? Puedes contarnos tu respuesta en barcolavadero.ovh. ¡Hasta la próxima!"
        segmentos.append(self.atenea.texto_a_segmento(cierre))

        # Ensamblar audio
        bloque = sum(segmentos, AudioSegment.silent(duration=500))
        ruta = "output/artista_oculto.mp3"
        bloque.export(ruta, format="mp3")
        print(f"🎭 Sección 'El artista oculto' exportada a {ruta}")

        return ruta, texto_total
