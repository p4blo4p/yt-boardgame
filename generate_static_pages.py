#!/usr/bin/env python3
"""
Generador de páginas estáticas para YT BoardGame
Convierte los datos JSON en páginas HTML estáticas para GitHub Pages
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import logging

# Configuración
VIDEOS_DATA_FILE = "videos_juegos_mesa.json"
CHANNELS_CONFIG_FILE = "channels_config.json"
OUTPUT_DIR = "dist"
TEMPLATES_DIR = "templates"

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    """Limpia el directorio de salida."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger.info(f"Directorio {OUTPUT_DIR} limpiado y creado")

def generate_static_page(videos_data: Dict[str, Any], channels_data: Dict[str, Any]) -> str:
    """Genera la página principal HTML estática."""
    
    # Calcular estadísticas
    total_channels = len(channels_data.get('ingles', {})) + len(channels_data.get('espanol', {}))
    total_videos = 0
    for idioma in videos_data.values():
        if isinstance(idioma, dict):
            for canal_videos in idioma.values():
                if isinstance(canal_videos, list):
                    total_videos += len(canal_videos)
    
    # Obtener fecha de última actualización
    last_update = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT BoardGame - Canales de Juegos de Mesa e IA</title>
    <meta name="description" content="Directorio curado de canales de YouTube sobre juegos de mesa e inteligencia artificial. Descubre los mejores canales organizados por idioma.">
    <meta name="keywords" content="juegos de mesa, YouTube, canales, IA, inteligencia artificial, board games, reviews">
    <link rel="canonical" href="https://p4blo4p.github.io/yt-boardgame-static/">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .header h1 {{
            color: white;
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .header p {{
            color: #f0f0f0;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }}

        .last-update {{
            color: #e0e0e0;
            font-size: 0.9rem;
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
        }}

        .stat-item {{
            text-align: center;
            background: rgba(255, 255, 255, 0.15);
            padding: 15px;
            border-radius: 10px;
        }}

        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #fff;
            display: block;
        }}

        .stat-label {{
            font-size: 0.9rem;
            color: #f0f0f0;
        }}

        .language-section {{
            margin-bottom: 50px;
        }}

        .language-header {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 25px;
        }}

        .language-title {{
            font-size: 2rem;
            color: white;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 30px;
            border-radius: 25px;
            backdrop-filter: blur(5px);
        }}

        .channels-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            padding: 0 10px;
        }}

        .channel-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
            display: block;
        }}

        .channel-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
            background: rgba(255, 255, 255, 1);
        }}

        .channel-name {{
            font-size: 1.4rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            text-align: center;
        }}

        .channel-url {{
            color: #e74c3c;
            font-size: 0.9rem;
            text-align: center;
            word-break: break-all;
            opacity: 0.8;
            margin-bottom: 15px;
        }}

        .videos-info {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            color: #495057;
            font-size: 0.9rem;
            margin-top: 15px;
        }}

        .videos-list {{
            margin-top: 15px;
            max-height: 200px;
            overflow-y: auto;
        }}

        .video-item {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
        }}

        .video-item:hover {{
            border-color: #007bff;
            box-shadow: 0 2px 8px rgba(0, 123, 255, 0.15);
        }}

        .video-title {{
            font-size: 0.95rem;
            font-weight: 500;
            color: #2c3e50;
            margin-bottom: 5px;
            line-height: 1.4;
        }}

        .video-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: #6c757d;
        }}

        .video-views {{
            background: #e9ecef;
            padding: 2px 8px;
            border-radius: 12px;
        }}

        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            color: white;
        }}

        .footer p {{
            margin-bottom: 10px;
        }}

        .footer a {{
            color: #f0f0f0;
            text-decoration: none;
            padding: 5px 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            transition: all 0.3s ease;
        }}

        .footer a:hover {{
            background: rgba(255, 255, 255, 0.2);
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .channels-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats {{
                flex-direction: column;
                gap: 15px;
            }}
        }}

        .loading {{
            text-align: center;
            color: white;
            font-size: 1.2rem;
            margin: 50px 0;
        }}

        .error {{
            background: rgba(231, 76, 60, 0.9);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🎲 YT BoardGame</h1>
            <p>Directorio curado de canales de YouTube sobre juegos de mesa e inteligencia artificial</p>
            <div class="last-update">📅 Última actualización: {last_update}</div>
        </header>

        <div class="stats">
            <div class="stat-item">
                <span class="stat-number">{total_channels}</span>
                <span class="stat-label">Total de Canales</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{total_videos}</span>
                <span class="stat-label">Videos Recientes</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{len(channels_data.get('ingles', {}))}</span>
                <span class="stat-label">Canales en Inglés</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{len(channels_data.get('espanol', {}))}</span>
                <span class="stat-label">Canales en Español</span>
            </div>
        </div>

        <main>"""

    # Generar secciones de canales
    for idioma, canales in channels_data.items():
        if not canales:
            continue
            
        flag = "🇺🇸" if idioma == "ingles" else "🇪🇸"
        idioma_titulo = "Inglés" if idioma == "ingles" else "Español"
        
        html_content += f"""
            <!-- Sección de Canales en {idioma_titulo} -->
            <section class="language-section">
                <div class="language-header">
                    <h2 class="language-title">{flag} Canales en {idioma_titulo}</h2>
                </div>
                <div class="channels-grid">"""
        
        for nombre_canal, url_canal in canales.items():
            # Obtener videos del canal
            videos_canal = videos_data.get(idioma, {}).get(nombre_canal, [])
            num_videos = len(videos_canal)
            
            html_content += f"""
                    <div class="channel-card">
                        <div class="channel-name">{nombre_canal}</div>
                        <div class="channel-url">{url_canal.replace('https://www.youtube.com/@', '@')}</div>
                        <div class="videos-info">
                            📹 {num_videos} videos recientes
                        </div>
                        <div class="videos-list">"""
            
            # Mostrar algunos videos recientes
            if videos_canal:
                for i, video in enumerate(videos_canal[:5]):  # Mostrar solo los primeros 5
                    if i < 3:  # Solo mostrar los primeros 3 expandidos
                        views = video.get('visualizaciones', 0)
                        if views >= 1000000:
                            views_str = f"{views/1000000:.1f}M"
                        elif views >= 1000:
                            views_str = f"{views/1000:.0f}K"
                        else:
                            views_str = str(views)
                        
                        html_content += f"""
                            <div class="video-item">
                                <div class="video-title">{video.get('titulo', 'Sin título')}</div>
                                <div class="video-meta">
                                    <span>👁️ {views_str} vistas</span>
                                    <span>📅 {video.get('fecha_subida', 'N/A')}</span>
                                </div>
                            </div>"""
                
                if num_videos > 5:
                    html_content += f"""
                            <div class="video-item" style="background: #f8f9fa; text-align: center; color: #6c757d;">
                                Y {num_videos - 5} videos más...
                            </div>"""
            
            html_content += """
                        </div>
                    </div>"""
        
        html_content += """
                </div>
            </section>"""

    html_content += """
        </main>

        <footer class="footer">
            <p>💡 Proyecto automatizado con GitHub Actions | Extracción diaria de videos</p>
            <p>🔗 <a href="https://github.com/p4blo4p/yt-boardgame" target="_blank">Código Fuente</a> | 
               <a href="https://github.com/p4blo4p/yt-boardgame-extractor" target="_blank">Extractor</a> | 
               <a href="https://youtube.com" target="_blank">YouTube</a></p>
            <p style="font-size: 0.8rem; opacity: 0.8;">Generado automáticamente por YT BoardGame Extractor</p>
        </footer>
    </div>

    <script>
        // Animaciones y interactividad
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🎲 YT BoardGame Static cargado correctamente');
            
            // Animación de entrada para las tarjetas
            const cards = document.querySelectorAll('.channel-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });

            // Expandir/colapsar videos al hacer clic
            const videoLists = document.querySelectorAll('.videos-list');
            videoLists.forEach(list => {
                const videos = list.querySelectorAll('.video-item');
                if (videos.length > 3) {
                    for (let i = 3; i < videos.length; i++) {
                        videos[i].style.display = 'none';
                    }
                    
                    const toggleBtn = document.createElement('div');
                    toggleBtn.className = 'video-item';
                    toggleBtn.style.background = '#007bff';
                    toggleBtn.style.color = 'white';
                    toggleBtn.style.cursor = 'pointer';
                    toggleBtn.style.textAlign = 'center';
                    toggleBtn.textContent = `📖 Ver todos los ${videos.length} videos`;
                    
                    let expanded = false;
                    toggleBtn.addEventListener('click', () => {
                        expanded = !expanded;
                        for (let i = 3; i < videos.length; i++) {
                            videos[i].style.display = expanded ? 'block' : 'none';
                        }
                        toggleBtn.textContent = expanded ? `📖 Ocultar videos` : `📖 Ver todos los ${videos.length} videos`;
                    });
                    
                    list.appendChild(toggleBtn);
                }
            });
        });
    </script>
</body>
</html>"""
    
    return html_content

def generate_videos_json_page(videos_data: Dict[str, Any]) -> str:
    """Genera una página JSON simple con todos los datos."""
    json_content = json.dumps(videos_data, ensure_ascii=False, indent=2)
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datos JSON - YT BoardGame</title>
    <style>
        body {{
            font-family: 'Monaco', 'Consolas', monospace;
            background: #1e1e1e;
            color: #d4d4d4;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #252526;
            border-radius: 8px;
            overflow: hidden;
        }}
        .header {{
            background: #007acc;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .json-content {{
            padding: 20px;
            overflow: auto;
            max-height: 80vh;
        }}
        pre {{
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .back-link {{
            display: inline-block;
            background: #007acc;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .back-link:hover {{
            background: #005a9e;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Datos JSON - YT BoardGame</h1>
            <p>Datos completos de videos extraídos</p>
        </div>
        <div class="json-content">
            <a href="index.html" class="back-link">← Volver al inicio</a>
            <pre>{json_content}</pre>
        </div>
    </div>
</body>
</html>"""
    return html_content

def main():
    """Función principal del generador."""
    logger.info("🚀 Iniciando generación de páginas estáticas")
    
    # Cargar datos
    videos_data = load_json_data(VIDEOS_DATA_FILE)
    channels_data = load_json_data(CHANNELS_CONFIG_FILE)
    
    if not videos_data or not channels_data:
        logger.error("❌ No se pudieron cargar los datos necesarios")
        return False
    
    # Limpiar directorio de salida
    clean_output_dir()
    
    # Generar página principal
    logger.info("📄 Generando página principal...")
    main_html = generate_static_page(videos_data, channels_data)
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(main_html)
    
    # Generar página JSON
    logger.info("📊 Generando página JSON...")
    json_html = generate_videos_json_page(videos_data)
    
    with open(os.path.join(OUTPUT_DIR, "data.html"), 'w', encoding='utf-8') as f:
        f.write(json_html)
    
    # Copiar archivo JSON directamente
    logger.info("📁 Copiando archivo JSON...")
    shutil.copy2(VIDEOS_DATA_FILE, os.path.join(OUTPUT_DIR, "videos.json"))
    
    logger.info("✅ Páginas estáticas generadas exitosamente en el directorio 'dist/'")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)