# -*- coding: utf-8 -*-
"""
Объектная модель баскетбольной площадки (лаб. 1–2) и расширения по методичке лаб. 3–9:
connect / emulate, валидация, Heater, Logger (MongoDB), анализ и данные для графика.
"""

from __future__ import annotations

import abc
import random
import re
from typing import Any, Dict, List, Optional

class Thing(abc.ABC):
    """Базовая «вещь» (лаб. 1): getStatus; для лаб. 3+ — emulate и connect."""

    def __init__(self, thing_id: str, name: str) -> None:
        self.id = thing_id
        self.name = name

    @abc.abstractmethod
    def getStatus(self) -> str:
        pass

    def emulate(self) -> None:
        """Лаб. 3: имитация обновления показаний (как рис. 12 методички)."""
        pass

    def connect(self, request: Any = None) -> Dict[str, Any]:
        """Лаб. 3–6: обмен с интерфейсом; возвращает dict для json.dumps в app.py."""
        raise NotImplementedError


class ScoreSensor(Thing):
    def __init__(self, thing_id: str, name: str, is_goal: bool = False) -> None:
        super().__init__(thing_id, name)
        self.is_goal = is_goal

    def getStatus(self) -> str:
        return "ScoreSensor[" + self.id + "]: is_goal=" + str(self.is_goal)

    def emulate(self) -> None:
        self.is_goal = random.choice([True, False])

    def connect(self, request: Any = None) -> Dict[str, Any]:
        self.emulate()
        return {"id": self.id, "value": 1 if self.is_goal else 0, "is_goal": self.is_goal}

    def connect_with_commands(self, request: Any) -> Dict[str, Any]:
        """Лаб. 4–5: команда из интерфейса (например коррекция)."""
        if request is not None:
            raw = request.args.get("value", "")
            try:
                v = int(float(raw))
                self.is_goal = bool(v)
            except ValueError:
                print("ScoreSensor: ожидалось число 0/1, получено:", type(raw).__name__)
        return {"power": "on", "is_goal": self.is_goal}


class ZoneSensor(Thing):
    ZONES = ("three-point-arc", "paint", "midcourt", "baseline")

    def __init__(self, thing_id: str, name: str, zone: str) -> None:
        super().__init__(thing_id, name)
        self.zone = zone

    def getStatus(self) -> str:
        return "ZoneSensor[" + self.id + "]: zone=" + self.zone

    def emulate(self) -> None:
        self.zone = random.choice(self.ZONES)

    def connect(self, request: Any = None) -> Dict[str, Any]:
        self.emulate()
        return {"id": self.id, "value": self.zone, "zone": self.zone}

    def connect_with_commands(self, request: Any) -> Dict[str, Any]:
        """Лаб. 5: строка — проверка регулярным выражением."""
        if request is None:
            return {"zone": self.zone}
        raw = request.args.get("value", "") or ""
        if re.fullmatch(r"[a-z0-9\-]+", raw):
            self.zone = raw
        else:
            print("ZoneSensor: недопустимая зона (нужны латиница, цифры, дефис):", repr(raw))
        return {"power": "on", "zone": self.zone}


class EnvSensor(Thing):
    def __init__(self, thing_id: str, name: str, temperature: float, light_lux: float) -> None:
        super().__init__(thing_id, name)
        self.temperature = float(temperature)
        self.lightLux = float(light_lux)

    def getStatus(self) -> str:
        return (
            "EnvSensor["
            + self.id
            + "]: t="
            + str(round(self.temperature, 1))
            + ", lux="
            + str(int(self.lightLux))
        )

    def emulate(self) -> None:
        self.temperature = round(random.uniform(18.0, 28.0), 1)
        self.lightLux = float(random.randint(300, 600))

    def connect(self, request: Any = None) -> Dict[str, Any]:
        """Мониторинг (лаб. 3): как Sensor в методичке — поле value для ajax."""
        self.emulate()
        return {
            "id": self.id,
            "value": self.temperature,
            "temperature": self.temperature,
            "lightLux": int(self.lightLux),
        }

    def connect_with_commands(self, request: Any) -> Dict[str, Any]:
        """Лаб. 5–6: float из запроса (try/except как рис. 25)."""
        if request is None:
            return {"power": "on", "value": self.temperature}
        raw = request.args.get("value", "")
        try:
            self.temperature = float(raw)
            self.temperature = round(self.temperature, 1)
        except ValueError:
            print(
                "EnvSensor: не удалось привести к float, тип:",
                type(raw).__name__,
                "значение:",
                repr(raw),
            )
        return {"power": "on", "value": self.temperature}


class Scoreboard(Thing):
    def __init__(self, thing_id: str, name: str, score_a: int = 0, score_b: int = 0, timer_sec: int = 0) -> None:
        super().__init__(thing_id, name)
        self.scoreA = score_a
        self.scoreB = score_b
        self.timerSec = timer_sec

    def getStatus(self) -> str:
        return (
            "Scoreboard["
            + self.id
            + "]: "
            + str(self.scoreA)
            + ":"
            + str(self.scoreB)
            + ", t="
            + str(self.timerSec)
        )

    def emulate(self) -> None:
        self.timerSec += random.randint(0, 2)
        if random.random() < 0.3:
            self.scoreA += 1

    def connect(self, request: Any = None) -> Dict[str, Any]:
        self.emulate()
        return {
            "id": self.id,
            "value": self.scoreA,
            "scoreA": self.scoreA,
            "scoreB": self.scoreB,
            "timer": self.timerSec,
        }

    def connect_with_commands(self, request: Any) -> Dict[str, Any]:
        if request is None:
            return {"scoreA": self.scoreA, "scoreB": self.scoreB}
        raw = request.args.get("value", "")
        try:
            parts = raw.split("-")
            if len(parts) == 2:
                self.scoreA = int(parts[0])
                self.scoreB = int(parts[1])
        except ValueError:
            print("Scoreboard: ожидался формат A-B для счёта")
        return {"power": "on", "scoreA": self.scoreA, "scoreB": self.scoreB}


class Heater:
    """Лаб. 6: обогреватель по температуре (класс Heater, рис. 27)."""

    def __init__(self, name: str, switch_on_temperature: float) -> None:
        self.name = name
        self.power = "Off"
        self.switch_on_temperature = switch_on_temperature

    def connect(self) -> Dict[str, Any]:
        return {"heater_power": self.power}

    def auto_power(self, temperature: float) -> None:
        self.power = "On" if temperature < self.switch_on_temperature else "Off"


class CourtDataStore:
    def __init__(self) -> None:
        self.events: List[str] = []
        self.telemetry: List[str] = []

    def saveEvent(self, data: Any) -> None:
        self.events.append("event=" + repr(data))

    def saveTelemetry(self, data: Any) -> None:
        self.telemetry.append("telemetry=" + repr(data))

    def getRecords(self) -> List[str]:
        return self.events + self.telemetry


class MainControlUnit:
    def __init__(self, things: List[Thing], store: CourtDataStore, scoreboard: Scoreboard) -> None:
        self.things = things
        self.store = store
        self.scoreboard = scoreboard

    def collectData(self) -> None:
        for t in self.things:
            self.store.saveTelemetry({"id": t.id, "status": t.getStatus()})

    def calculateScore(self) -> None:
        for t in self.things:
            if isinstance(t, ScoreSensor) and t.is_goal:
                self.scoreboard.scoreA += 1
                self.store.saveEvent({"type": "basket", "points": self.scoreboard.scoreA})
                break

    def updateScoreboard(self) -> None:
        self.scoreboard.timerSec += 1
