# agents/lector_feed.py

import os
import feedparser
from datetime import datetime, timedelta
import re
import html

class LectorFeed:
    def __init__(self, archivo_feeds: str = "feeds.txt"):
        self.archivo_feeds = archivo_feeds

    def leer_urls(self):
        try:
            with open(self.archivo_feeds, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Archivo de feeds '{self.archivo_feeds}' no encontrado.")
            return []

    def limpiar_texto(self, texto: str) -> str:
        texto = re.sub(r'<[^>]+>', '', texto)  # etiquetas HTML
        texto = html.unescape(texto)
        texto = re.sub(r'[#@]\S+', '', texto)  # hashtags y menciones
        texto = re.sub(r'[^\w\s.,;:()¡!¿?"\'%-]', '', texto)  # emojis y símbolos
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto

    def obtener_noticias(self, min_items: int = 5):
        urls = self.leer_urls()
        noticias = []
        ahora = datetime.now()

        for url in urls:
            try:
                feed = feedparser.parse(url)
                sitio = getattr(feed.feed, 'title', 'Sitio desconocido')

                for entrada in feed.entries:
                    # Fecha de publicación (si está disponible)
                    fecha = ahora
                    if hasattr(entrada, 'published_parsed') and entrada.published_parsed:
                        fecha = datetime(*entrada.published_parsed[:6])

                    if (ahora - fecha) > timedelta(days=1):
                        continue  # solo noticias recientes

                    contenido = getattr(entrada, 'summary', getattr(entrada, 'description', ''))
                    if contenido:
                        texto = self.limpiar_texto(contenido)
                        noticias.append((sitio, texto))
            except Exception as e:
                print(f"Error procesando {url}: {e}")

        # Si no se obtuvieron suficientes, coger los más recientes sin filtrar por fecha
        if len(noticias) < min_items:
            print(f"Solo se encontraron {len(noticias)} noticias recientes. Recuperando más antiguas...")
            for url in urls:
                try:
                    feed = feedparser.parse(url)
                    sitio = getattr(feed.feed, 'title', 'Sitio desconocido')

                    for entrada in feed.entries:
                        contenido = getattr(entrada, 'summary', getattr(entrada, 'description', ''))
                        if contenido:
                            texto = self.limpiar_texto(contenido)
                            noticias.append((sitio, texto))
                        if len(noticias) >= min_items:
                            break
                except:
                    continue

        return noticias[:min_items]
