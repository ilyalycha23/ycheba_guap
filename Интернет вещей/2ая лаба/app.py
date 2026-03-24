from flask import Flask, render_template

import things

app = Flask(__name__)


def demo_iot_cycle():
    store = things.CourtDataStore()
    score_sensor = things.ScoreSensor("ss1", "Кольцо команды A", is_goal=True)
    zone_sensor = things.ZoneSensor("zs1", "Разметка площадки", "three-point-arc")
    env_sensor = things.EnvSensor("es1", "Микроклимат зала", 22.5, 420.0)
    scoreboard = things.Scoreboard("sb1", "Табло арены", 0, 0, 0)

    all_things = [score_sensor, zone_sensor, env_sensor, scoreboard]
    unit = things.MainControlUnit(all_things, store, scoreboard)

    print("=== Демонстрация: collectData() ===")
    unit.collectData()

    print("=== Демонстрация: calculateScore() ===")
    unit.calculateScore()

    print("=== Демонстрация: updateScoreboard() ===")
    unit.updateScoreboard()

    print("=== CourtDataStore.getRecords() ===")
    records = store.getRecords()
    print("Записей в хранилище:", len(records))


@app.route("/", methods=["GET"])
def hello_world():
    demo_iot_cycle()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
