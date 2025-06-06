# crew/demo_crew.py

from crewai import Agent, Task, Crew
from agents.lector_feed import LectorFeed
from agents.traductor_resumidor import TraductorResumidor
from agents.locutor import Locutor
import os

# === Adaptar funciones para Crew ===

def leer_noticia(input_text=None):
    lector = LectorFeed("feeds.txt")
    noticias = lector.obtener_noticias(min_items=1)
    return noticias[0][1]  # Devuelve texto limpio de la primera noticia

def resumir_texto(input_text):
    traductor = TraductorResumidor()
    return traductor.traducir_y_resumir(input_text)

def generar_audio(input_text):
    locutor = Locutor()
    locutor.texto_a_audio(input_text, "demo_output")
    return "🎧 Audio generado en output/demo_output.mp3"

# === Crear agentes CrewAI ===

lector_agente = Agent(
    role="Lector de noticias",
    goal="Leer noticias de arte desde feeds RSS",
    backstory="Un lector experto en seleccionar noticias recientes sobre arte para el podcast.",
    verbose=True,
    allow_delegation=False,
    tools=[leer_noticia]
)

resumidor_agente = Agent(
    role="Editor de contenido",
    goal="Traducir y resumir noticias de forma clara para el oyente",
    backstory="Especializado en adaptar noticias a un lenguaje cercano, cultural y atractivo.",
    verbose=True,
    allow_delegation=False,
    tools=[resumir_texto]
)

locutor_agente = Agent(
    role="Narrador del podcast",
    goal="Convertir textos en voz para el archivo de audio final",
    backstory="Locutor digital entrenado en español europeo para podcast culturales.",
    verbose=True,
    allow_delegation=False,
    tools=[generate_audio := generar_audio]
)

# === Definir tarea principal ===

tarea = Task(
    description="Seleccionar una noticia de arte, traducirla y resumirla, y generar el audio final",
    expected_output="Un archivo de audio llamado 'demo_output.mp3' con el resumen locutado.",
    agents=[lector_agente, resumidor_agente, locutor_agente]
)

crew = Crew(tasks=[tarea], verbose=True)
