"""
Лабораторная работа №9 - Визуализация данных с Chart.js
Вариант: Умное игровое поле для игры в баскетбол
"""
from flask import Flask, request, render_template, jsonify
import things
import json

app = Flask(__name__)
shot_sensor = things.Sensor('points', 'shot_sensor')
scoreboard = things.Scoreboard('Scoreboard1', 25)
logger = things.Logger('iot_basketball_db')


@app.route('/connect')
def connect():
    response = shot_sensor.connect(request)
    if isinstance(response, dict) and shot_sensor.value and isinstance(shot_sensor.value, int):
        scoreboard.auto_display(shot_sensor.value)
        logger.insert_score(shot_sensor.value)
    return json.dumps(response) if isinstance(response, dict) else response


@app.route('/connect_scoreboard')
def connect_scoreboard():
    response = scoreboard.connect()
    return json.dumps(response)


@app.route('/api/chart_data')
def chart_data():
    """API для Chart.js - возвращает данные в JSON"""
    records = logger.get_all_scores()
    labels = [r['timeStamp'] for r in records]
    data = [r['Points'] for r in records]
    return jsonify({'labels': labels, 'data': data})


@app.route('/history')
def history():
    data = logger.get_all_scores()
    return render_template('history.html', records=data)


@app.route('/chart')
def chart():
    """Страница с графиком Chart.js"""
    return render_template('chart.html')


@app.route('/')
def hello_world():
    return render_template('sensor_emulator.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
