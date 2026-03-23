"""
Лабораторная работа №5 - Валидация данных датчика
Вариант: Умное игровое поле для игры в баскетбол
"""
from flask import Flask, request, render_template
import things

app = Flask(__name__)
shot_sensor = things.Sensor('points', 'shot_sensor')


@app.route('/connect')
def connect():
    return shot_sensor.connect(request)


@app.route('/')
def hello_world():
    return render_template('sensor_emulator.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
