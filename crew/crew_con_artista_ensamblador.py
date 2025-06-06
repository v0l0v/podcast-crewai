# crew/crew_con_artista_ensamblador.py

from crewai import Agent, Task, Crew
from agents.lector_feed import LectorFeed
from agents.traductor_resumidor import TraductorResumidor
from agents.locutor import Locutor
from agents.generador_artista import GeneradorArtista
from langchain.tools import Tool
import os

# === Funciones conectadas a tus agentes ===

def leer_noticia(input_text=None):
    lector = LectorFeed("feeds.txt")
    noticias = lector.obtener_noticias(min_items=1)
    return noticias[0][1]

def resumir_texto(input_text):
    traductor = TraductorResumidor()
    return traductor.traducir_y_resumir(input_text)

def generar_audio(input_text):
    locutor = Locutor()
    locutor.texto_a_audio(input_text, "demo_output")
    return "🎧 Audio generado en output/demo_output.mp3"

def generar_artista_oculto(input_text=None):
    print("\n🎭 Generando bloque del artista oculto...")
    generador = GeneradorArtista()
    ruta, contenido = generador.generar_bloque_automatico()
    return f"🎨 Bloque generado en {ruta}\nArtista: {contenido['artista']}"

def ensamblar_podcast(input_text=None):
    print("\n🎛️ Ensamblando podcast final...\n")
    from ensamblador import ensamblar_podcast as ejecutar
    ejecutar()
    return "✅ Podcast final exportado con audio, Markdown y HTML."

# === Agentes ===

lector_agente = Agent(
    role="Lector de noticias",
    goal="Seleccionar noticias recientes de arte",
    backstory="Extrae contenido artístico desde feeds para el podcast.",
    verbose=True,
    allow_delegation=False,
    tools=[Tool.from_function(func=leer_noticia, name="Leer Noticia")]
)

resumidor_agente = Agent(
    role="Editor de noticias",
    goal="Resumir las noticias para una audiencia general",
    backstory="Especialista en adaptar noticias culturales a formato hablado.",
    verbose=True,
    allow_delegation=False,
    tools=[Tool.from_function(func=resumir_texto, name="Resumir Texto")]
)

locutor_agente = Agent(
    role="Locutor digital",
    goal="Convertir texto en audio para el episodio diario",
    backstory="Voz profesional entrenada para podcast de arte.",
    verbose=True,
    allow_delegation=False,
    tools=[Tool.from_function(func=generar_audio, name="Generar Audio")]
)

artista_agente = Agent(
    role="Narrador del artista oculto",
    goal="Crear un bloque narrado con pistas y reflexión sobre un artista misterioso",
    backstory="Se comunica como el propio artista, con voz distinta y profundidad emocional.",
    verbose=True,
    allow_delegation=False,
    tools=[Tool.from_function(func=generar_artista_oculto, name="Generar Artista Oculto")]
)

productor_agente = Agent(
    role="Productor del podcast",
    goal="Combinar todas las partes en un episodio completo con audio y texto",
    backstory="Coordina las secciones generadas y las publica como episodio final.",
    verbose=True,
    allow_delegation=False,
    tools=[Tool.from_function(func=ensamblar_podcast, name="Ensamblar Podcast")]
)

# === Tareas ===

tarea_noticia = Task(
    description="Leer una noticia, resumirla y generar el audio locutado.",
    expected_output="Un archivo 'demo_output.mp3' con el resumen.",
    agents=[lector_agente, resumidor_agente, locutor_agente]
)

tarea_artista = Task(
    description="Generar el bloque completo del artista oculto con voz y contenido narrativo.",
    expected_output="Archivo 'artista_oculto.mp3' con pistas, reflexión, resolución y consejo.",
    agents=[artista_agente]
)

tarea_ensamblaje = Task(
    description="Unir introducción, noticias, artista oculto y despedida en un archivo .mp3, .md y .html.",
    expected_output="Episodio completo del podcast exportado en /output.",
    agents=[productor_agente]
)

# === Crew Final ===

crew = Crew(
    tasks=[
        tarea_noticia,
        tarea_artista,
        tarea_ensamblaje
    ],
    verbose=True
)
