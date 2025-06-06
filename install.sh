#!/bin/bash

echo "🚀 Iniciando instalación del entorno para podcast-crewai..."

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements_actualizado.txt

echo "✅ Entorno listo. Usa 'source venv/bin/activate' para activarlo."