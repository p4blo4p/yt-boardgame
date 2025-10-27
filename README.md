# 🎲 YT BoardGame

Una aplicación web Python que funciona como un directorio curado de canales de YouTube especializados en **juegos de mesa e inteligencia artificial**. La aplicación extrae automáticamente videos recientes de estos canales y los presenta en una interfaz web organizada por idioma.

## ✨ Características

- 🌐 **Interfaz web moderna** con diseño responsive
- 🤖 **Extracción automática** de videos usando yt-dlp
- 🌍 **Organización por idioma** (inglés y español)
- 📱 **Design responsive** adaptable a móviles
- 🔄 **API REST** para integración con otros servicios
- ⏰ **Actualización automática** con GitHub Actions
- 📊 **Estadísticas en tiempo real** de canales y videos

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/p4blo4p/yt-boardgame.git
cd yt-boardgame
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar canales (opcional):**
Edita el archivo `channels_config.json` para personalizar los canales:
```json
{
  "ingles": {
    "Tu Canal": "https://www.youtube.com/@tu_canal"
  },
  "espanol": {
    "Tu Canal": "https://www.youtube.com/@tu_canal"
  }
}
```

4. **Ejecutar extracción inicial:**
```bash
python extraer_info_canales.py
```

5. **Iniciar la aplicación web:**
```bash
python app.py
```

6. **Abrir en el navegador:**
Visita `http://localhost:5000`

## 📁 Estructura del Proyecto

```
yt-boardgame/
├── app.py                          # Aplicación web Flask principal
├── extraer_info_canales.py         # Script de extracción de datos
├── channels_config.json           # Configuración de canales (JSON)
├── videos_juegos_mesa.json        # Datos de videos extraídos
├── requirements.txt               # Dependencias de Python
├── templates/
│   └── index.html                # Template HTML principal
├── README.md                      # Este archivo
└── .github/
    └── workflows/
        └── update_videos_data.yml # GitHub Actions para actualización automática
```

## 🔧 Configuración

### Variables de Configuración

En `extraer_info_canales.py` puedes ajustar:

```python
OUTPUT_FILE = "videos_juegos_mesa.json"           # Archivo de salida
EXTRACTION_INTERVAL_SECONDS = 24 * 3600          # Intervalo de extracción (24h)
MAX_VIDEOS_TO_CHECK_PER_CHANNEL = 10             # Videos a verificar por canal
MAX_VIDEOS_PER_CHANNEL = 200                     # Máximo de videos por canal
REQUEST_DELAY_SECONDS = 2                        # Delay entre requests (segundos)
```

### Personalizar Canales

Edita `channels_config.json` para:
- ➕ Agregar nuevos canales
- 🗑️ Eliminar canales existentes
- 🌍 Cambiar URLs o nombres
- 📝 Reorganizar por idiomas

**Ejemplo:**
```json
{
  "ingles": {
    "Nuevo Canal": "https://www.youtube.com/@nuevocanal"
  },
  "espanol": {
    "Canal Español": "https://www.youtube.com/@canalespanol"
  }
}
```

## 🌐 API Endpoints

La aplicación expone varios endpoints de API:

### GET /
**Página principal** - Interfaz web con canales organizados

### GET /api/canales
**Configuración de canales** - Devuelve la configuración JSON de canales
```bash
curl http://localhost:5000/api/canales
```

### GET /api/videos
**Datos de videos** - Devuelve todos los videos extraídos
```bash
curl http://localhost:5000/api/videos
```

### GET /health
**Estado del sistema** - Verifica el estado de la aplicación
```bash
curl http://localhost:5000/health
```

## 🔄 Automatización

### GitHub Actions
El proyecto incluye un workflow automático que:
- Ejecuta extracción de videos diariamente
- Actualiza el archivo `videos_juegos_mesa.json`
- Mantiene los datos siempre actualizados

### Extracción Manual
```bash
# Extraer videos una vez
python extraer_info_canales.py

# Ver logs de extracción
python extraer_info_canales.py 2>&1 | tee extraction.log
```

## 🛠️ Desarrollo

### Ejecutar en Modo Desarrollo
```bash
python app.py
# La aplicación estará disponible en http://localhost:5000
```

### Debugging
```bash
# Habilitar modo debug detallado
export FLASK_DEBUG=1
python app.py
```

### Logs
Los logs se muestran en la consola durante la ejecución:
```
2024-01-01 12:00:00 - INFO - Iniciando extracción de videos de canales de YouTube
2024-01-01 12:00:01 - INFO - Procesando canal The Dice Tower (ingles)
2024-01-01 12:00:05 - INFO - Canal The Dice Tower: 8 videos nuevos, 45 total
```

## 📊 Estadísticas y Métricas

La aplicación muestra:
- **Total de canales** monitoreados
- **Videos por canal** recientes
- **Distribución por idioma**
- **Estado de la última extracción**

## 🐛 Solución de Problemas

### Error: "Archivo no encontrado"
```bash
# Ejecutar extracción inicial
python extraer_info_canales.py
```

### Error: "JSON inválido"
```bash
# Verificar formato del JSON
python -m json.tool channels_config.json
```

### Error: "yt-dlp no encontrado"
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Error: "Puerto en uso"
```bash
# Cambiar puerto en app.py
app.run(debug=True, port=8080)
```

## 📝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Extracción de videos de YouTube
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [YouTube](https://youtube.com) - Plataforma de videos

## 📞 Soporte

Si encuentras problemas o tienes sugerencias:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Busca en los [Issues](https://github.com/p4blo4p/yt-boardgame/issues)
3. Crea un nuevo issue con detalles del problema

---

**¡Disfruta descubriendo nuevos canales de juegos de mesa e IA!** 🎲🤖

# yt-boardgame

¡Tienes toda la razón! Disculpa la omisión. Aquí tienes la lista actualizada con enlaces a los canales de YouTube:

**Canales de YouTube en Inglés sobre Juegos de Mesa**

| Canal                     | Descripción                                                                                                     | Enfoque Principal                                                                        | Estilo                                               | Enlace                                                                       |
| -------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------- |
| **The Dice Tower**        | Reseñas, partidas, noticias y listas de juegos de mesa. Uno de los canales más grandes y populares.           | Reseñas profundas, listas Top 10, noticias de la industria.                                | Profesional, informativo, a veces humorístico.       | [The Dice Tower](https://www.youtube.com/@TheDiceTower)                     |
| **Shut Up & Sit Down**    | Reseñas de juegos de mesa con un enfoque humorístico y entretenido.                                            | Reseñas con mucho humor, partidas comentadas.                                           | Humorístico, irreverente, creativo.                  | [Shut Up & Sit Down](https://www.youtube.com/@shutupandsitdown)                |
| **Tabletop (Wil Wheaton)** | Partidas grabadas con celebridades y creadores de juegos de mesa.                                           | Partidas completas, entrevistas a diseñadores.                                           | Entretenido, relajado, accesible.                   | [Tabletop (Wil Wheaton)](https://www.youtube.com/@tabletop)                  |
| **BoardGameGeek**        | Canal oficial de BoardGameGeek, la mayor base de datos de juegos de mesa.                                      | Noticias, previews, entrevistas, demostraciones.                                       | Informativo, profesional, directo.                  | [BoardGameGeek](https://www.youtube.com/@boardgamegeek)                       |
| **Gaming with Edo**      | Reseñas, tutoriales y partidas comentadas con un enfoque en juegos de mesa complejos y temáticos.            | Reseñas detalladas, tutoriales para juegos complejos.                                     | Analítico, profundo, bien producido.                | [Gaming with Edo](https://www.youtube.com/@GamingwithEdo)                    |
| **No Pun Included**      | Reseñas con un enfoque en juegos de mesa con mecánicas innovadoras y diseños artísticos.                      | Reseñas con opiniones fuertes, análisis de diseño.                                          | Inteligente, analítico, bien producido.            | [No Pun Included](https://www.youtube.com/@NoPunIncluded)                    |
| **Rhado Runs Through**     | Tutoriales en solitario de juegos de mesa, partidas y reseñas en profundidad.                                    | Tutoriales de juegos en solitario, explicaciones detalladas de reglas.                   | Didáctico, claro, enfocado en el juego en solitario. | [Rhado Runs Through](https://www.youtube.com/@rahdo)                          |
| **Heavy Cardboard**       | Enfoque en juegos de mesa complejos, pesados (eurogames) con reseñas y partidas.                                 | Reseñas de juegos pesados, análisis estratégico, discusiones profundas.                  | Analítico, técnico, enfocado en jugadores expertos.  | [Heavy Cardboard](https://www.youtube.com/@HeavyCardboard)                    |

**Canales de YouTube en Español sobre Juegos de Mesa**

| Canal                           | Descripción                                                                                               | Enfoque Principal                                                              | Estilo                                              | Enlace                                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Análisis Parálisis**            | Reseñas, tutoriales y partidas comentadas de juegos de mesa.                                            | Reseñas detalladas, tutoriales bien explicados, partidas divertidas.        | Informativo, amigable, entretenido.                | [Análisis Parálisis](https://www.youtube.com/@AnalisisParalisis)                |
| **El Dado Friki**                 | Noticias, reseñas, partidas y tutoriales de juegos de mesa.                                               | Noticias, reseñas, tutoriales, unboxing.                                       | Variado, informativo, bien producido.             | [El Dado Friki](https://www.youtube.com/@ElDadoFriki)                         |
| **Jugando con Ketty**            | Reseñas de juegos de mesa, tutoriales y partidas comentadas.                                             | Reseñas, partidas comentadas, tutoriales para juegos de dificultad variada. | Amigable, cercano, bien explicado.               | [Jugando con Ketty](https://www.youtube.com/@JugandoconKetty)                 |
| **Mesa para Dos**                | Reseñas y partidas comentadas de juegos de mesa, con un enfoque en juegos para dos jugadores.             | Reseñas de juegos para dos, partidas.                                         | Dinámico, entretenido, especializado en juegos 2P. | [Mesa para Dos](https://www.youtube.com/@MesaparaDos)                         |
| **Ciudadano Meeple**            | Noticias, reseñas, tutoriales y partidas comentadas de juegos de mesa.                                     | Noticias, reseñas, partidas, tutoriales.                                       | Informativo, variado, bien producido.             | [Ciudadano Meeple](https://www.youtube.com/@CiudadanoMeeple)                 |
| **Juegos de Mesa 221B**          | Reseñas y tutoriales de juegos de mesa con un enfoque en juegos temáticos y narrativos.                   | Reseñas de juegos temáticos, tutoriales detallados.                           | Temático, profundo, bien documentado.             | [Juegos de Mesa 221B](https://www.youtube.com/@JuegosdeMesa221B)              |
| **La Mazmorra de Pacheco**      | Reseñas de juegos de mesa, unboxings y partidas.                                                          | Reseñas, unboxings, partidas.                                                | Sencillo, directo, amigable.                      | [La Mazmorra de Pacheco](https://www.youtube.com/@lamazmorradepacheco)       |
| **La Guarida del Goblin**        | Reseñas, tutoriales y partidas comentadas de juegos de mesa, con un enfoque en juegos de rol.         | Reseñas, tutoriales, juegos de rol, miniaturas.                               | Variado, temático, enfocado en el mundo goblin.    | [La Guarida del Goblin](https://www.youtube.com/@LaGuaridadelGoblin)           |

**Nota:** Verifiqué los enlaces al momento de crear esta lista. Si alguno no funciona, por favor házmelo saber. ¡Espero que disfrutes explorando estos canales!


# AI
¡Perfecto! Aquí tienes la lista de canales de YouTube sobre Inteligencia Artificial en formato de tabla, separando los de habla inglesa y los de habla castellana:

**Canales de YouTube sobre IA (Inglés)**

| Idioma  | Canal                      | Enfoque Principal                                  | Audiencia Objetivo                            | Descripción/Destacado                                                  |
| :------ | :------------------------- | :------------------------------------------------- | :-------------------------------------------- | :--------------------------------------------------------------------- |
| Inglés  | **Lex Fridman Podcast**    | Entrevistas profundas (IA, Ciencia, Filosofía)     | General, Investigadores, Pensadores           | Conversaciones largas con líderes mundiales en IA y otros campos.      |
| Inglés  | **Two Minute Papers**      | Resúmenes visuales de investigación (IA, Gráficos) | Técnicos, Curiosos                              | Explicaciones claras y rápidas de papers complejos.                     |
| Inglés  | **Matt Wolfe**             | Noticias IA, Tutoriales prácticos (Herramientas)   | Usuarios generales, Negocios                  | Enfocado en cómo usar herramientas de IA (ChatGPT, Midjourney, etc.). |
| Inglés  | **AI Explained**           | Explicación de noticias y lanzamientos de IA       | General, Entusiastas                          | Desglosa novedades de IA de forma accesible.                           |
| Inglés  | **Yannic Kilcher**         | Análisis técnico profundo de papers de IA/ML       | Investigadores, Desarrolladores               | Entra en los detalles técnicos de la investigación en IA.              |
| Inglés  | **AssemblyAI**           | Contenido educativo (NLP, Speech AI), Tutoriales   | Desarrolladores, Técnicos                     | Contenido de calidad de una empresa de API de IA.                      |
| Inglés  | **Robert Scoble**          | Entrevistas, Visitas (Futurismo, IA, VR)           | Entusiastas, Industria                        | Visión "desde dentro" de laboratorios y empresas tecnológicas.       |
| Inglés  | **The Verge**              | Noticias y análisis de tecnología general (con IA) | Audiencia tecnológica general                 | Sólida cobertura de IA dentro de un medio tecnológico amplio.        |
| Inglés  | **WIRED**                  | Cultura tecnológica, Ética, Análisis (con IA)    | General, Interesados en cultura/sociedad      | Explora el impacto social y ético de la IA.                          |
| Inglés  | **ColdFusion**             | Mini-documentales sobre tecnología y negocios      | General, Negocios                             | Episodios bien producidos sobre tecnologías disruptivas como la IA.    |

**Canales de YouTube sobre IA (Castellano)**

| Idioma     | Canal                               | Enfoque Principal                                    | Audiencia Objetivo                            | Descripción/Destacado                                                    |
| :--------- | :---------------------------------- | :--------------------------------------------------- | :-------------------------------------------- | :----------------------------------------------------------------------- |
| Castellano | **DotCSV (Carlos Santana)**         | Explicación didáctica de IA, ML, Noticias            | Estudiantes, Desarrolladores, Curiosos        | Principal divulgador de IA en español, muy claro y entretenido.           |
| Castellano | **Nate Gentile**                    | Tecnología general, Hardware (cubre impacto IA)      | Entusiastas de la tecnología, Gamers          | Analiza el impacto de la IA, GPUs para IA, etc.                            |
| Castellano | **Xataka TV**                       | Noticias y análisis de tecnología general (con IA)   | Audiencia tecnológica general                 | Fuente principal de noticias de tecnología en español, con buena cobertura IA. |
| Castellano | **Ring R. A. (Inteligencia Artificial)** | Noticias IA, Tutoriales prácticos (Herramientas)     | Usuarios generales, Entusiastas               | Canal dedicado a noticias y tutoriales de herramientas de IA.              |
| Castellano | **Platzi**                          | Educación online (cursos IA, Programación)           | Estudiantes, Profesionales                    | Muchos vídeos gratuitos explicando conceptos y herramientas de IA.       |
| Castellano | **La Robot de Platón (Aldo Bartra)** | Divulgación científica general (incluye IA)          | Público general curioso                       | Aborda la IA desde una perspectiva científica amplia y ética.             |
| Castellano | **VisualPolitik**                   | Geopolítica, Economía (analiza impacto IA)           | Interesados en negocios y política            | Analiza el impacto estratégico y económico global de la IA.            |
| Castellano | **Antonio G. (Inteligencia Artificial)** | Noticias diarias IA, Tutoriales (Herramientas)       | Usuarios generales, Entusiastas               | Actualizaciones frecuentes y guías prácticas de herramientas.            |
| Castellano | **Edgar Krawetz (ia.channel)**      | Demostraciones prácticas de herramientas IA, Prompts | Usuarios que quieren aplicar IA              | Enfocado en el uso práctico y demos de herramientas variadas.            |
| Castellano | **David Bonilla (Bonillaware)**     | Comunidad Tech, Negocios (discute IA)                | Desarrolladores, Emprendedores                | Perspectiva sobre IA desde el mundo del desarrollo y negocio tech.      |

Espero que este formato te sea más útil para comparar los canales.
