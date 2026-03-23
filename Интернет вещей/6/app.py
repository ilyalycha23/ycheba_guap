"""
Лабораторная работа №6 - Интеллектуальный актуатор (табло счёта)
Вариант: Умное игровое поле для игры в баскетбол
"""
from flask import Flask, request, render_template
import things
import json

app = Flask(__name__)
shot_sensor = things.Sensor('points', 'shot_sensor')
scoreboard = things.Scoreboard('Scoreboard1', 25)  # порог 25 очков для подсветки


@app.route('/connect')
def connect():
    response = shot_sensor.connect(request)
    if isinstance(response, dict) and response.get("power") != "error" and shot_sensor.value and isinstance(shot_sensor.value, int):
        scoreboard.auto_display(shot_sensor.value)
    return json.dumps(response) if isinstance(response, dict) else response


@app.route('/connect_scoreboard')
def connect_scoreboard():
    response = scoreboard.connect()
    return json.dumps(response)


@app.route('/')
def hello_world():
    return render_template('sensor_emulator.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
