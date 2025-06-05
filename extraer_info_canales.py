import yt_dlp
import json
import time
from datetime import datetime, timezone
import os
import logging
from typing import Dict, List, Any, Optional, Set

# --- Configuración ---
OUTPUT_FILE = 'videos_juegos_mesa.json'
EXTRACTION_INTERVAL_SECONDS = 24 * 3600  # Extracción diaria
MAX_VIDEOS_TO_CHECK_PER_CHANNEL = 30      # Cuántos videos recientes revisar por canal para buscar nuevos
MAX_VIDEOS_PER_CHANNEL = 200              # Máximo de videos a guardar por canal en el JSON
REQUEST_DELAY_SECONDS = 2                 # Pausa entre peticiones a YouTube

CHANNELS = {
    "ingles": {
        "The Dice Tower": "https://www.youtube.com/@TheDiceTower",
        "Shut Up & Sit Down": "https://www.youtube.com/@shutupandsitdown",
        "Tabletop (Wil Wheaton)": "https://www.youtube.com/@tabletop", # Canal podría estar inactivo o tener contenido diferente ahora
        "BoardGameGeek": "https://www.youtube.com/@boardgamegeek",
        "Gaming with Edo": "https://www.youtube.com/@GamingwithEdo",
        "No Pun Included": "https://www.youtube.com/@NoPunIncluded",
        "Rhado Runs Through": "https://www.youtube.com/@rahdo",
        "Heavy Cardboard": "https://www.youtube.com/@HeavyCardboard"
    },
    "espanol": {
        "Análisis Parálisis": "https://www.youtube.com/@AnalisisParalisis",
        "El Dado Friki": "https://www.youtube.com/@ElDadoFriki",
        "Jugando con Ketty": "https://www.youtube.com/@JugandoconKetty",
        "Mesa para Dos": "https://www.youtube.com/@MesaparaDos",
        "Ciudadano Meeple": "https://www.youtube.com/@CiudadanoMeeple",
        "Juegos de Mesa 221B": "https://www.youtube.com/@JuegosdeMesa221B",
        "La Mazmorra de Pacheco": "https://www.youtube.com/@lamazmorradepacheco",
        "La Guarida del Goblin": "https://www.youtube.com/@LaGuaridadelGoblin"
    }
}

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _construir_info_video(entry: Dict[str, Any], canal_nombre: str, canal_url: str) -> Dict[str, Any]:
    """Construye el diccionario de información para un video."""
    return {
        'id': entry.get('id'),
        'title': entry.get('title'),
        'url': entry.get('original_url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
        'thumbnail': entry.get('thumbnail'),
        'channel_name': canal_nombre,
        'channel_url': canal_url,
        'fetched_at': datetime.now(timezone.utc).isoformat()
    }

def extraer_videos_recientes_canal(
    canal_nombre: str,
    canal_url: str,
    ids_videos_existentes: Set[str]
) -> List[Dict[str, Any]]:
    """
    Extrae información de los videos más recientes de un canal que no están en ids_videos_existentes.
    """
    ydl_opts = {
        'extract_flat': True,  # Solo metadatos, no descarga
        'quiet': True,
        'ignoreerrors': True,  # Continúa si un video individual falla
        'playlistend': MAX_VIDEOS_TO_CHECK_PER_CHANNEL, # Solo los N más recientes
    }

    nuevos_videos: List[Dict[str, Any]] = []
    logging.info(f"Extrayendo información de '{canal_nombre}' ({canal_url})...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # info_dict es la información del canal/playlist
            info_dict = ydl.extract_info(canal_url, download=False)

            if not info_dict:
                logging.warning(f"No se pudo obtener información para el canal '{canal_nombre}'.")
                return []

            # info_dict['entries'] es la lista de videos
            entries = info_dict.get('entries')
            if not entries:
                logging.info(f"No se encontraron videos recientes o el canal '{canal_nombre}' está vacío/no accesible.")
                return []

            # yt_dlp devuelve los videos más recientes primero
            for entry in entries:
                video_id = entry.get('id')
                if not video_id:
                    logging.warning(f"Video sin ID en '{canal_nombre}', entrada: {entry.get('title', 'N/A')}")
                    continue

                if video_id not in ids_videos_existentes:
                    video_info = _construir_info_video(entry, info_dict.get('channel', canal_nombre), info_dict.get('channel_url', canal_url))
                    nuevos_videos.append(video_info)
                # No necesitamos 'else: break' porque 'playlistend' limita la cantidad de videos
                # y queremos añadir todos los nuevos dentro de ese rango.

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Error de yt-dlp al extraer de '{canal_nombre}': {e}")
    except Exception as e:
        logging.error(f"Error inesperado al extraer de '{canal_nombre}': {e}", exc_info=True)

    logging.info(f"Encontrados {len(nuevos_videos)} nuevos videos para '{canal_nombre}'.")
    return nuevos_videos # Los más recientes estarán al principio

def guardar_datos_videos(data: Dict[str, Any]) -> None:
    """Guarda los datos de los videos en el archivo JSON."""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Datos guardados en '{OUTPUT_FILE}'.")
    except IOError as e:
        logging.error(f"Error al guardar datos en '{OUTPUT_FILE}': {e}")

def cargar_videos_existentes() -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """Carga los datos de videos existentes desde el archivo JSON."""
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error al cargar '{OUTPUT_FILE}': {e}. Se usará una estructura vacía.")
    return {"ingles": {}, "espanol": {}} # Estructura por defecto

def actualizar_canales_por_idioma(
    canales_a_procesar: Dict[str, str],
    datos_existentes_del_idioma: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Actualiza la información de los videos para un conjunto de canales de un idioma.
    """
    datos_actualizados_idioma: Dict[str, List[Dict[str, Any]]] = {}

    for nombre_canal, url_canal in canales_a_procesar.items():
        videos_antiguos_canal = datos_existentes_del_idioma.get(nombre_canal, [])
        ids_existentes = {video['id'] for video in videos_antiguos_canal if video.get('id')}

        nuevos_videos = extraer_videos_recientes_canal(nombre_canal, url_canal, ids_existentes)

        # Combinar nuevos videos (al principio) con los antiguos, y limitar la cantidad total
        lista_videos_combinada = nuevos_videos + videos_antiguos_canal
        datos_actualizados_idioma[nombre_canal] = lista_videos_combinada[:MAX_VIDEOS_PER_CHANNEL]

        time.sleep(REQUEST_DELAY_SECONDS) # Ser amable con los servidores de YouTube

    return datos_actualizados_idioma

def ejecutar_extraccion_unica():
    """Ejecuta un solo ciclo de extracción de información."""
    logging.info("Iniciando ciclo de extracción de videos (ejecución única)...")
    datos_guardados = cargar_videos_existentes()
    nuevos_datos_globales: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}

    for idioma, canales_del_idioma in CHANNELS.items():
        logging.info(f"Procesando canales en '{idioma}'...")
        datos_existentes_idioma = datos_guardados.get(idioma, {})
        nuevos_datos_globales[idioma] = actualizar_canales_por_idioma(
            canales_del_idioma,
            datos_existentes_idioma
        )

    guardar_datos_videos(nuevos_datos_globales)
    logging.info("Ciclo de extracción (ejecución única) completado.")

if __name__ == '__main__':
    # Para ejecutar localmente con el bucle:
    # try:
    #     main_loop()
    # except KeyboardInterrupt:
    #     logging.info("Proceso interrumpido por el usuario.")
    # except Exception as e:
    #     logging.critical(f"Error crítico en el bucle principal: {e}", exc_info=True)

    # Para ejecutar una sola vez (ideal para GitHub Actions si se llamara así)
    try:
        ejecutar_extraccion_unica() # Llamar a esta función si la tienes
    except Exception as e:
        logging.critical(f"Error crítico durante la extracción única: {e}", exc_info=True)
        raise # Propagar el error para que la Action falle si es necesario
