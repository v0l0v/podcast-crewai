# 🎙️ Proyecto Podcast CrewAI

Este proyecto genera un podcast automatizado de arte usando agentes inteligentes con CrewAI.

---

## 📦 Estructura del proyecto

```
podcast-crewai/
├── agents/
├── crew/
│   └── crew_con_artista_ensamblador.py
├── output/
├── feeds.txt
├── ensamblador.py
├── podcastgenerator.py
├── requirements_actualizado.txt
├── install.sh
├── .env.example
├── venv/
```

---

## 🛠️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/podcast-crewai.git
cd podcast-crewai
```

2. Ejecuta el instalador:

```bash
bash install.sh
```

3. Activa el entorno virtual:

```bash
source venv/bin/activate
```

---

## ⚙️ Configura tus variables de entorno

Copia el archivo de ejemplo y edítalo:

```bash
cp .env.example .env
```

Luego abre `.env` y ajusta:

- `GOOGLE_APPLICATION_CREDENTIALS=./gen-lang-client-xxx.json`
- `IDIOMA_OBJETIVO=es`
- `MIN_ITEMS=1`

(Agrega también `OPENAI_API_KEY=...` si usas modelos de OpenAI)

---

## 🚀 Ejecutar la Crew completa

Con el entorno activo:

```bash
python -c "from crew.crew_con_artista_ensamblador import crew; crew.kickoff()"
```

Esto generará:

- 📰 Noticias de arte resumidas y locutadas
- 🎭 Sección del “artista oculto”
- 🎧 Podcast final ensamblado en `/output`

---

## 🖥️ Interfaz gráfica

Ejecuta:

```bash
python podcastgenerator.py
```

Podrás configurar parámetros y lanzar todo con un solo clic desde la GUI.

---

¡Listo para producir arte sonoro automatizado! 🎨🎙️