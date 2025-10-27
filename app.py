from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal que muestra los canales de YouTube organizados por idioma."""
    try:
        # Cargar datos de videos desde el archivo JSON
        with open('videos_juegos_mesa.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Cargar configuración de canales
        with open('channels_config.json', 'r', encoding='utf-8') as f:
            channels_config = json.load(f)
        
        return render_template('index.html', 
                             canales_ingles=channels_config['ingles'], 
                             canales_espanol=channels_config['espanol'],
                             videos_data=data)
    
    except FileNotFoundError as e:
        return f"Error: Archivo no encontrado - {e}. Asegúrate de ejecutar primero 'extraer_info_canales.py'", 500
    except json.JSONDecodeError as e:
        return f"Error: JSON inválido - {e}", 500
    except Exception as e:
        return f"Error interno del servidor: {e}", 500

@app.route('/api/canales')
def api_canales():
    """API endpoint que devuelve la configuración de canales en JSON."""
    try:
        with open('channels_config.json', 'r', encoding='utf-8') as f:
            channels_config = json.load(f)
        return jsonify(channels_config)
    except FileNotFoundError:
        return jsonify({"error": "Archivo de configuración no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/videos')
def api_videos():
    """API endpoint que devuelve los datos de videos en JSON."""
    try:
        with open('videos_juegos_mesa.json', 'r', encoding='utf-8') as f:
            videos_data = json.load(f)
        return jsonify(videos_data)
    except FileNotFoundError:
        return jsonify({"error": "Datos de videos no encontrados"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Endpoint de salud para verificar el estado de la aplicación."""
    return jsonify({"status": "ok", "message": "La aplicación está funcionando correctamente"})

if __name__ == '__main__':
    # Verificar que los archivos necesarios existan
    required_files = ['channels_config.json', 'videos_juegos_mesa.json']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"⚠️  Archivos faltantes: {missing_files}")
        print("Ejecuta 'python extraer_info_canales.py' para generar los datos iniciales")
    
    print("🚀 Iniciando aplicación yt-boardgame...")
    print("📡 Servidor disponible en: http://localhost:5000")
    print("🔗 API endpoints disponibles:")
    print("   - GET /api/canales - Configuración de canales")
    print("   - GET /api/videos - Datos de videos")
    print("   - GET /health - Estado de la aplicación")
    
    app.run(debug=True, host='0.0.0.0', port=5000)