import yt_dlp
import json
import time
from datetime import datetime, timedelta

# Configuración
OUTPUT_FILE = 'videos_juegos_mesa.json'
EXTRACTION_INTERVAL = 24 * 3600  # Extracción diaria (en segundos)

canales_ingles = {
    "The Dice Tower": "https://www.youtube.com/@TheDiceTower",
    "Shut Up & Sit Down": "https://www.youtube.com/@shutupandsitdown",
    "Tabletop (Wil Wheaton)": "https://www.youtube.com/@tabletop",
    "BoardGameGeek": "https://www.youtube.com/@boardgamegeek",
    "Gaming with Edo": "https://www.youtube.com/@GamingwithEdo",
    "No Pun Included": "https://www.youtube.com/@NoPunIncluded",
    "Rhado Runs Through": "https://www.youtube.com/@rahdo",
    "Heavy Cardboard": "https://www.youtube.com/@HeavyCardboard"
}

canales_espanol = {
    "Análisis Parálisis": "https://www.youtube.com/@AnalisisParalisis",
    "El Dado Friki": "https://www.youtube.com/@ElDadoFriki",
    "Jugando con Ketty": "https://www.youtube.com/@JugandoconKetty",
    "Mesa para Dos": "https://www.youtube.com/@MesaparaDos",
    "Ciudadano Meeple": "https://www.youtube.com/@CiudadanoMeeple",
    "Juegos de Mesa 221B": "https://www.youtube.com/@JuegosdeMesa221B",
    "La Mazmorra de Pacheco": "https://www.youtube.com/@lamazmorradepacheco",
    "La Guarida del Goblin": "https://www.youtube.com/@LaGuaridadelGoblin"
}

def extraer_info_canal(canal_url, ultimo_id=None):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(canal_url, download=False)
            videos = []
            for entry in info_dict['entries']:
                if ultimo_id and entry.get('id') == ultimo_id:
                    break
                video_info = {
                    'title': entry.get('title'),
                    'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                    'thumbnail': entry.get('thumbnail'),
                    'channel_name': info_dict.get('channel'),
                    'channel_url': canal_url
                }
                videos.append(video_info)
            return videos
        except Exception as e:
            print(f"Error al extraer información de {canal_url}: {e}")
            return []

def guardar_videos(data):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def cargar_videos():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'ingles': {}, 'espanol': {}}

def obtener_info_todos_canales(canales, data_anterior):
    data = {}
    for nombre_canal, url_canal in canales.items():
        print(f"Extrayendo información de {nombre_canal}...")
        ultimo_id = data_anterior.get(nombre_canal, [{}])[-1].get('id') if data_anterior.get(nombre_canal) else None
        nuevos_videos = extraer_info_canal(url_canal, ultimo_id)
        data[nombre_canal] = nuevos_videos + data_anterior.get(nombre_canal, [])
        time.sleep(2)
    return data

def main():
    while True:
        data_anterior = cargar_videos()
        info_ingles = obtener_info_todos_canales(canales_ingles, data_anterior.get('ingles', {}))
        info_espanol = obtener_info_todos_canales(canales_espanol, data_anterior.get('espanol', {}))
        data = {'ingles': info_ingles, 'espanol': info_espanol}
        guardar_videos(data)
        print("Información extraída y guardada en videos_juegos_mesa.json")
        time.sleep(EXTRACTION_INTERVAL)

if __name__ == '__main__':
    main()
