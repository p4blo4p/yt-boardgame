from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('videos_juegos_mesa.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('index.html', canales_ingles=data['ingles'], canales_espanol=data['espanol'])

if __name__ == '__main__':
    app.run(debug=True)
