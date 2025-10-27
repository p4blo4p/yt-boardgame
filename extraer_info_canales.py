import yt_dlp
import json
import time
from datetime import datetime, timedelta
import os
import logging
from typing import Dict, List, Any, Optional, Set

# Configuración
OUTPUT_FILE = "videos_juegos_mesa.json"
EXTRACTION_INTERVAL_SECONDS = 24 * 3600  # Extracción diaria
MAX_VIDEOS_TO_CHECK_PER_CHANNEL = 10  # Configurado para pruebas rápidas, se puede aumentar a 30
MAX_VIDEOS_PER_CHANNEL = 200  # Máximo de videos por canal a guardar en JSON
REQUEST_DELAY_SECONDS = 2  # Pausa entre requests a YouTube
CHANNELS_CONFIG_FILE = "channels_config.json"

# Cargar configuración de canales desde JSON
def cargar_configuracion_canales():
    """Carga la configuración de canales desde el archivo JSON."""
    try:
        with open(CHANNELS_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Archivo de configuración {CHANNELS_CONFIG_FILE} no encontrado.")
        return {"ingles": {}, "espanol": {}}
    except json.JSONDecodeError as e:
        logging.error(f"Error al decodificar JSON en {CHANNELS_CONFIG_FILE}: {e}")
        return {"ingles": {}, "espanol": {}}

# Configuración de canales cargada dinámicamente
CHANNELS = cargar_configuracion_canales()

def _construir_info_video(video_data: Dict[str, Any], nombre_canal: str, url_canal: str) -> Dict[str, Any]:
    """Construye la información de un video en el formato estándar."""
    return {
        "id": video_data.get("id", ""),
        "titulo": video_data.get("title", ""),
        "url": video_data.get("webpage_url", ""),
        "thumbnail": video_data.get("thumbnail", ""),
        "nombre_canal": nombre_canal,
        "url_canal": url_canal,
        "fecha_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duracion": video_data.get("duration", 0),
        "fecha_subida": video_data.get("upload_date", ""),
        "visualizaciones": video_data.get("view_count", 0)
    }

def extraer_videos_recientes_canal(url_canal: str, nombre_canal: str, ids_existentes: Set[str]) -> List[Dict[str, Any]]:
    """Extrae videos recientes de un canal específico."""
    videos = []
    
    opciones = {
        'quiet': True,
        'ignoreerrors': True,
        'playlistend': MAX_VIDEOS_TO_CHECK_PER_CHANNEL,
        'dateafter': (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
    }
    
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url_canal, download=False)
            
            if 'entries' in info:
                for entrada in info['entries']:
                    if entrada and entrada.get('id') not in ids_existentes:
                        video_info = _construir_info_video(entrada, nombre_canal, url_canal)
                        videos.append(video_info)
            
            # Pausa entre requests
            time.sleep(REQUEST_DELAY_SECONDS)
            
    except yt_dlp.utils.DownloadError as e:
        logging.warning(f"Error al extraer videos del canal {nombre_canal}: {e}")
    except Exception as e:
        logging.error(f"Error inesperado al procesar canal {nombre_canal}: {e}")
    
    return videos

def guardar_datos_videos(datos: Dict[str, Any]) -> None:
    """Guarda los datos de videos en un archivo JSON."""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        logging.info(f"Datos guardados exitosamente en {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Error al guardar datos: {e}")

def cargar_videos_existentes() -> Dict[str, Any]:
    """Carga videos existentes del archivo JSON."""
    try:
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logging.info("Archivo de datos no existe, creando estructura nueva")
            return {"ingles": {}, "espanol": {}}
    except (json.JSONDecodeError, IOError) as e:
        logging.warning(f"Error al cargar datos existentes: {e}")
        return {"ingles": {}, "espanol": {}}

def actualizar_canales_por_idioma(idioma: str, datos_existentes: Dict[str, Any], canales: Dict[str, str]) -> Dict[str, Any]:
    """Actualiza los datos para un idioma específico."""
    nuevos_datos = datos_existentes.get(idioma, {})
    
    for nombre_canal, url_canal in canales.items():
        logging.info(f"Procesando canal {nombre_canal} ({idioma})")
        
        # Obtener IDs existentes
        ids_existentes = set()
        if nombre_canal in nuevos_datos:
            ids_existentes = {video.get("id", "") for video in nuevos_datos[nombre_canal]}
            ids_existentes.discard("")  # Remover strings vacíos
        
        # Extraer videos nuevos
        videos_nuevos = extraer_videos_recientes_canal(url_canal, nombre_canal, ids_existentes)
        
        # Combinar con videos existentes
        videos_existentes = nuevos_datos.get(nombre_canal, [])
        todos_los_videos = videos_existentes + videos_nuevos
        
        # Limitar número de videos por canal
        todos_los_videos = todos_los_videos[:MAX_VIDEOS_PER_CHANNEL]
        
        nuevos_datos[nombre_canal] = todos_los_videos
        
        logging.info(f"Canal {nombre_canal}: {len(videos_nuevos)} videos nuevos, {len(todos_los_videos)} total")
    
    return nuevos_datos

def ejecutar_extraccion_unica():
    """Ejecuta una extracción única de videos de todos los canales."""
    logging.info("Iniciando extracción de videos de canales de YouTube")
    
    # Cargar datos existentes
    datos = cargar_videos_existentes()
    
    # Procesar canales en inglés
    if "ingles" in CHANNELS:
        logging.info("Procesando canales en inglés")
        datos["ingles"] = actualizar_canales_por_idioma("ingles", datos, CHANNELS["ingles"])
    
    # Procesar canales en español
    if "espanol" in CHANNELS:
        logging.info("Procesando canales en español")
        datos["espanol"] = actualizar_canales_por_idioma("espanol", datos, CHANNELS["espanol"])
    
    # Guardar datos actualizados
    guardar_datos_videos(datos)
    
    logging.info("Extracción completada exitosamente")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    ejecutar_extraccion_unica()