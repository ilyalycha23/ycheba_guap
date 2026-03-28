# -*- coding: utf-8 -*-
"""
Лаб. 2–6 по методичке: обогреватель Heater и auto_power; без журнала MongoDB (лаб. 7+).
"""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

import things

app = Flask(__name__)

env_sensor = things.EnvSensor("es1", "Микроклимат зала", 22.0, 400.0)
score_sensor = things.ScoreSensor("ss1", "Кольцо команды A", is_goal=False)
zone_sensor = things.ZoneSensor("zs1", "Разметка площадки", "three-point-arc")
scoreboard = things.Scoreboard("sb1", "Табло арены", 0, 0, 0)
heater = things.Heater("Обогреватель зала", 22.0)

store = things.CourtDataStore()
mcu = things.MainControlUnit(
    [score_sensor, zone_sensor, env_sensor, scoreboard],
    store,
    scoreboard,
)


def demo_iot_cycle() -> None:
    print("=== collectData ===")
    mcu.collectData()
    print("=== calculateScore ===")
    mcu.calculateScore()
    print("=== updateScoreboard ===")
    mcu.updateScoreboard()
    print("=== getRecords ===", len(store.getRecords()))


@app.route("/monitor/env")
def monitor_env():
    return jsonify(env_sensor.connect())


@app.route("/monitor/score")
def monitor_score():
    return jsonify(score_sensor.connect())


@app.route("/monitor/zone")
def monitor_zone():
    return jsonify(zone_sensor.connect())


@app.route("/monitor/board")
def monitor_board():
    return jsonify(scoreboard.connect())


@app.route("/connect")
def connect():
    """Лаб. 4–6: команда температуры, auto_power обогревателя."""
    response = env_sensor.connect_with_commands(request)
    heater.auto_power(env_sensor.temperature)
    response["heater_power"] = heater.power
    return jsonify(response)


@app.route("/connect_heater")
def connect_heater():
    return jsonify(heater.connect())


@app.route("/command/score")
def command_score():
    return jsonify(score_sensor.connect_with_commands(request))


@app.route("/command/zone")
def command_zone():
    return jsonify(zone_sensor.connect_with_commands(request))


@app.route("/command/board")
def command_board():
    return jsonify(scoreboard.connect_with_commands(request))


@app.route("/lab2")
def lab2_page():
    demo_iot_cycle()
    return render_template("lab2.html")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/emulator")
def emulator_page():
    return render_template("sensor_emulator.html")


if __name__ == "__main__":
    app.run(debug=True)
