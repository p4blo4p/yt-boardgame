#!/usr/bin/env python3
"""
Generador de páginas estáticas para YT BoardGame
Convierte los datos JSON en páginas HTML estáticas para GitHub Pages usando Jinja2.
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import logging

from jinja2 import Environment, FileSystemLoader, select_autoescape

# Configuración
VIDEOS_DATA_FILE = "videos_juegos_mesa.json"
CHANNELS_CONFIG_FILE = "channels_config.json"
OUTPUT_DIR = "dist"
TEMPLATES_DIR = "templates"
STATIC_DIR_NAME = "static" # Nombre de la carpeta estática dentro de templates

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar Jinja2
# FileSystemLoader busca plantillas en TEMPLATES_DIR
# select_autoescape previene ataques XSS escapando HTML si es necesario
env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

def load_json_data(file_path: str) -> Dict[str, Any]:
    """Carga datos desde un archivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON en {file_path}: {e}")
        return {}

def clean_output_dir():
    """Limpia el directorio de salida y recrea las subcarpetas necesarias."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        logger.info(f"Directorio {OUTPUT_DIR} limpiado")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, STATIC_DIR_NAME), exist_ok=True)
    logger.info(f"Directorio {OUTPUT_DIR} y subcarpetas creadas")

def format_views(views: int) -> str:
    """Formatea el número de vistas a K, M, etc."""
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views / 1_000:.0f}K"
    else:
        return str(views)

def generate_index_page(videos_data: Dict[str, Any], channels_data: Dict[str, Any]):
    """Genera la página principal HTML estática usando la plantilla index.html."""
    logger.info("📄 Generando página principal (index.html)...")
    
    template = env.get_template('index.html')

    # Calcular estadísticas
    total_channels = sum(len(c) for c in channels_data.values() if isinstance(c, dict))
    total_videos = 0
    for lang_videos in videos_data.values():
        if isinstance(lang_videos, dict):
            for channel_videos in lang_videos.values():
                if isinstance(channel_videos, list):
                    total_videos += len(channel_videos)
    
    last_update = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Preparar datos para la plantilla
    rendered_html = template.render(
        last_update=last_update,
        total_channels=total_channels,
        total_videos=total_videos,
        channels_ingles_count=len(channels_data.get('ingles', {})),
        channels_espanol_count=len(channels_data.get('espanol', {})),
        channels_data=channels_data,
        videos_data=videos_data,
        format_views=format_views # Pasar la función de formato a la plantilla
    )
    
    output_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    logger.info(f"Página principal guardada en {output_path}")

def generate_data_json_page(videos_data: Dict[str, Any]):
    """Genera una página HTML para mostrar los datos JSON brutos."""
    logger.info("📊 Generando página de datos JSON (data.html)...")
    
    template = env.get_template('data_json.html')
    json_content = json.dumps(videos_data, ensure_ascii=False, indent=2)

    rendered_html = template.render(
        json_content=json_content
    )
    
    output_path = os.path.join(OUTPUT_DIR, "data.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    logger.info(f"Página de datos JSON guardada en {output_path}")

def copy_static_assets():
    """Copia los archivos CSS y JS de la carpeta templates/static a dist/static."""
    source_static_dir = os.path.join(TEMPLATES_DIR, STATIC_DIR_NAME)
    destination_static_dir = os.path.join(OUTPUT_DIR, STATIC_DIR_NAME)

    if os.path.exists(source_static_dir):
        for item in os.listdir(source_static_dir):
            s = os.path.join(source_static_dir, item)
            d = os.path.join(destination_static_dir, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
                logger.info(f"Copiado archivo estático: {item}")
            # Si hubiera subdirectorios dentro de static, esto los copiaría también
            # elif os.path.isdir(s):
            #     shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        logger.warning(f"No se encontró la carpeta estática en {source_static_dir}")

def main():
    """Función principal del generador."""
    logger.info("🚀 Iniciando generación de páginas estáticas")
    
    # Cargar datos
    videos_data = load_json_data(VIDEOS_DATA_FILE)
    channels_data = load_json_data(CHANNELS_CONFIG_FILE)
    
    if not videos_data or not channels_data:
        logger.error("❌ No se pudieron cargar los datos necesarios")
        return False
    
    # Limpiar directorio de salida y crear estructura
    clean_output_dir()
    
    # Generar página principal
    generate_index_page(videos_data, channels_data)
    
    # Generar página JSON
    generate_data_json_page(videos_data)
    
    # Copiar archivo JSON directamente para acceso directo
    logger.info("📁 Copiando archivo JSON crudo (videos.json)...")
    shutil.copy2(VIDEOS_DATA_FILE, os.path.join(OUTPUT_DIR, "videos.json"))

    # Copiar archivos estáticos (CSS, JS)
    copy_static_assets()
    
    logger.info("✅ Páginas estáticas generadas exitosamente en el directorio 'dist/'")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)