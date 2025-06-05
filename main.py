from agents.lector_feed import LectorFeed
from agents.traductor_resumidor import TraductorResumidor
from agents.locutor import Locutor
from tools.transiciones import Transiciones
from dotenv import load_dotenv
from pydub import AudioSegment
import os

def main():
    load_dotenv()

    lector = LectorFeed("feeds.txt")
    noticias = lector.obtener_noticias(min_items=3)

    traductor = TraductorResumidor()
    locutor = Locutor()
    transiciones = Transiciones("assets")

    podcast = AudioSegment.empty()

    for i, (sitio, texto) in enumerate(noticias, 1):
        resumen = traductor.traducir_y_resumir(texto)
        print(f"\n📖 {sitio}: {resumen}\n")

        audio_resumen = locutor.texto_a_segmento(resumen)
        efecto = transiciones.obtener_efecto()

        podcast += audio_resumen + efecto

    # Guardar el podcast completo
    os.makedirs("output", exist_ok=True)
    salida = "output/podcast_completo.mp3"
    podcast.export(salida, format="mp3")
    print(f"\n✅ Podcast final exportado a {salida}")

if __name__ == "__main__":
    main()
