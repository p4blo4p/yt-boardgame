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
MAX_VIDEOS_TO_CHECK_PER_CHANNEL = 10 # Reducido para pruebas rápidas, puedes aumentarlo a 30
MAX_VIDEOS_PER_CHANNEL = 200              # Máximo de videos a guardar por canal en el JSON
REQUEST_DELAY_SECONDS = 2                 # Pausa entre peticiones a YouTube

CHANNELS = {
    "ingles": {
        "The Dice Tower": "https://www.youtube.com/@TheDiceTower",
        "Shut Up & Sit Down": "https://www.youtube.com/@shutupandsitdown",
        # "Tabletop (Wil Wheaton)": "https://www.youtube.com/@tabletop",
        "BoardGameGeek": "https://www.youtube.com/@boardgamegeek",
        # "Gaming with Edo": "https://www.youtube.com/@GamingwithEdo",
        # "No Pun Included": "https://www.youtube.com/@NoPunIncluded",
        # "Rhado Runs Through": "https://www.youtube.com/@rahdo",
        # "Heavy Cardboard": "https://www.youtube.com/@HeavyCardboard"
    },
    "espanol": {
        "Análisis Parálisis": "https://www.youtube.com/@AnalisisParalisis",
        # "El Dado Friki": "https://www.youtube.com/@ElDadoFriki",
        # "Jugando con Ketty": "https://www.youtube.com/@JugandoconKetty",
        # "Mesa para Dos": "https://www.youtube.com/@MesaparaDos",
        # "Ciudadano Meeple": "https://www.youtube.com/@CiudadanoMeeple",
        # "Juegos de Mesa 221B": "https://www.youtube.com/@JuegosdeMesa221B",
        # "La Mazmorra de Pacheco": "https://www.youtube.com/@lamazmorradepacheco",
        # "La Guarida del Goblin": "https://www.youtube.com/@LaGuaridadelGoblin"
    }
}

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _construir_info_video(entry: Dict[str, Any], canal_nombre_global: str, canal_url_global: str) -> Dict[str, Any]:
    """Construye el diccionario de información para un video."""
    video_id = entry.get('id')
    return {
        'id': video_id,
        'title': entry.get('title'),
        'url': entry.get('original_url') or (f"https://www.youtube.com/watch?v={video_id}" if video_id else None),
        'thumbnail': entry.get('thumbnail'), # Esta es la URL del thumbnail por defecto
        # entry.get('thumbnails') es una lista de thumbnails de diferentes tamaños si necesitas más control
        'channel_name': canal_nombre_global, # Usamos el nombre del canal que estamos procesando
        'channel_url': canal_url_global,   # Usamos la URL del canal que estamos procesando
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'duration': entry.get('duration'), # Opcional: duración en segundos
        'upload_date': entry.get('upload_date'), # Opcional: YYYYMMDD
        'view_count': entry.get('view_count') # Opcional
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
        # 'extract_flat': True, # COMENTADO/ELIMINADO para obtener thumbnails y más detalles
        'quiet': True,
        'ignoreerrors': True,
        'playlistend': MAX_VIDEOS_TO_CHECK_PER_CHANNEL,
        'dateafter': (datetime.now() - timedelta(days=90)).strftime('%Y%m%d') # Opcional: solo videos de los últimos X días
    }

    nuevos_videos: List[Dict[str, Any]] = []
    logging.info(f"Extrayendo detalles de videos de '{canal_nombre}' ({canal_url})...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # info_dict aquí es la info de la playlist/canal
            info_dict = ydl.extract_info(canal_url, download=False)

            if not info_dict:
                logging.warning(f"No se pudo obtener información para el canal '{canal_nombre}'.")
                return []

            entries = info_dict.get('entries')
            if not entries:
                logging.info(f"No se encontraron videos (o entradas válidas) recientes para el canal '{canal_nombre}'.")
                return []

            # El nombre del canal y la URL se toman de la información de la playlist/canal principal
            # 'uploader' suele ser más fiable que 'channel' para el nombre del canal en info_dict de playlists
            nombre_canal_real = info_dict.get('uploader', info_dict.get('channel', canal_nombre))
            url_canal_real = info_dict.get('uploader_url', info_dict.get('channel_url', canal_url))


            for entry in entries:
                if not entry: # yt-dlp puede devolver None en la lista de entries con ignoreerrors
                    logging.warning(f"Entrada de video vacía encontrada en '{nombre_canal_real}'. Saltando.")
                    continue

                video_id = entry.get('id')
                if not video_id:
                    logging.warning(f"Video sin ID en '{nombre_canal_real}', título: {entry.get('title', 'N/A')}. Saltando.")
                    continue
                
                if entry.get('thumbnail') is None:
                    logging.debug(f"Video '{video_id}' ('{entry.get('title')}') en '{nombre_canal_real}' no tiene thumbnail URL directamente en 'thumbnail'. Revisando 'thumbnails'.")
                    # A veces 'thumbnail' es None pero 'thumbnails' (lista) existe.
                    # _construir_info_video usa entry.get('thumbnail'), que está bien para el thumbnail por defecto.

                if video_id not in ids_videos_existentes:
                    video_info = _construir_info_video(entry, nombre_canal_real, url_canal_real)
                    nuevos_videos.append(video_info)

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Error de yt-dlp al extraer de '{canal_nombre}': {e}")
    except Exception as e:
        logging.error(f"Error inesperado al extraer de '{canal_nombre}': {e}", exc_info=True)

    logging.info(f"Encontrados {len(nuevos_videos)} nuevos videos para '{canal_nombre}'.")
    return nuevos_videos

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
                data = json.load(f)
                # Asegurar estructura esperada
                if not isinstance(data, dict): return {"ingles": {}, "espanol": {}}
                if "ingles" not in data: data["ingles"] = {}
                if "espanol" not in data: data["espanol"] = {}
                return data
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error al cargar '{OUTPUT_FILE}': {e}. Se usará una estructura vacía.")
    return {"ingles": {}, "espanol": {}}

def actualizar_canales_por_idioma(
    canales_a_procesar: Dict[str, str],
    datos_existentes_del_idioma: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, List[Dict[str, Any]]]:
    datos_actualizados_idioma: Dict[str, List[Dict[str, Any]]] = {}

    for nombre_canal_config, url_canal_config in canales_a_procesar.items():
        # Usamos nombre_canal_config como clave en nuestro JSON, pero la info real del canal vendrá de yt-dlp
        videos_antiguos_canal = datos_existentes_del_idioma.get(nombre_canal_config, [])
        ids_existentes = {video['id'] for video in videos_antiguos_canal if video.get('id')}

        nuevos_videos = extraer_videos_recientes_canal(nombre_canal_config, url_canal_config, ids_existentes)

        # Combinar nuevos videos (al principio) con los antiguos, y limitar la cantidad total
        # Los nuevos videos ya vienen con el nombre de canal y URL actualizados por yt-dlp si es necesario
        lista_videos_combinada = nuevos_videos + videos_antiguos_canal
        
        # Asegurarse de que el nombre del canal en la clave del diccionario es el que usamos en la config
        datos_actualizados_idioma[nombre_canal_config] = lista_videos_combinada[:MAX_VIDEOS_PER_CHANNEL]

        time.sleep(REQUEST_DELAY_SECONDS)

    return datos_actualizados_idioma

def ejecutar_extraccion_unica():
    logging.info("Iniciando ciclo de extracción de videos (ejecución única)...")
    datos_guardados = cargar_videos_existentes()
    nuevos_datos_globales: Dict[str, Dict[str, List[Dict[str, Any]]]] = {"ingles": {}, "espanol": {}}

    for idioma, canales_del_idioma_config in CHANNELS.items():
        logging.info(f"Procesando canales en '{idioma}'...")
        datos_existentes_idioma = datos_guardados.get(idioma, {})
        nuevos_datos_globales[idioma] = actualizar_canales_por_idioma(
            canales_del_idioma_config,
            datos_existentes_idioma
        )

    guardar_datos_videos(nuevos_datos_globales)
    logging.info("Ciclo de extracción (ejecución única) completado.")

if __name__ == '__main__':
    from datetime import timedelta # Asegurar que timedelta está importado si se usa 'dateafter'
    try:
        ejecutar_extraccion_unica()
    except Exception as e:
        logging.critical(f"Error crítico durante la extracción única: {e}", exc_info=True)
        # raise # Descomentar si se quiere que la Action falle explícitamente
