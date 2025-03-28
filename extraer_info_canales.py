import yt_dlp
import json
import time

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

def extraer_info_canal(canal_url, num_videos=10):  # Limitar a los 10 videos más recientes por defecto
    ydl_opts = {
        'extract_flat': True,  # No extrae información detallada de cada video.
        'quiet': True,  # Reduce la salida en la consola.
        'force_generic_extractor': True, #Usa el extractor generico
        'playlistend': num_videos  # Limita el número de videos a extraer.
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(canal_url, download=False)
            videos = []
            for entry in info_dict['entries']:
                video_info = {
                    'title': entry.get('title'),
                    'url':  f"https://www.youtube.com/watch?v={entry.get('id')}", #Construye el enlace del video
                    'thumbnail': entry.get('thumbnail'),  # URL de la miniatura
                    'channel_name': info_dict.get('channel'), #Nombre del canal
                    'channel_url': canal_url  #URL del canal
                }
                videos.append(video_info)
            return videos
        except Exception as e:
            print(f"Error al extraer información de {canal_url}: {e}")
            return []

def obtener_info_todos_canales(canales, num_videos=10):
    data = {}
    for nombre_canal, url_canal in canales.items():
        print(f"Extrayendo información de {nombre_canal}...")
        data[nombre_canal] = extraer_info_canal(url_canal, num_videos)
        time.sleep(2)  # Pausa de 2 segundos entre cada extracción para evitar ser bloqueado por la API de YouTube
    return data

if __name__ == '__main__':
    info_ingles = obtener_info_todos_canales(canales_ingles)
    info_espanol = obtener_info_todos_canales(canales_espanol)

    # Guarda la información en un archivo JSON (opcional).
    with open('videos_juegos_mesa.json', 'w', encoding='utf-8') as f:
        json.dump({'ingles': info_ingles, 'espanol': info_espanol}, f, indent=4, ensure_ascii=False)

    print("Información extraída y guardada en videos_juegos_mesa.json")
