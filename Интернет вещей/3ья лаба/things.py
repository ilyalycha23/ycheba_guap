from __future__ import annotations

import abc
import random
from typing import Any, Dict, List, Optional

class Thing(abc.ABC):

    def __init__(self, thing_id: str, name: str) -> None:
        self.id = thing_id
        self.name = name

    @abc.abstractmethod
    def getStatus(self) -> str:
        pass

    def emulate(self) -> None:
        pass

    def connect(self, request: Any = None) -> Dict[str, Any]:
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
        self.emulate()
        return {
            "id": self.id,
            "value": self.temperature,
            "temperature": self.temperature,
            "lightLux": int(self.lightLux),
        }


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
