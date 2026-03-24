from abc import ABC, abstractmethod


class Thing(ABC):
    def __init__(self, thing_id, name):
        self.id = thing_id
        self.name = name

    @abstractmethod
    def getStatus(self):
        pass


class ScoreSensor(Thing):
    def __init__(self, thing_id, name, is_goal=False):
        super().__init__(thing_id, name)
        self.is_goal = is_goal

    def getStatus(self):
        msg = "ScoreSensor[" + self.id + "]: is_goal=" + str(self.is_goal)
        print("getStatus() —", msg)
        return msg


class ZoneSensor(Thing):
    def __init__(self, thing_id, name, zone):
        super().__init__(thing_id, name)
        self.zone = zone

    def getStatus(self):
        msg = "ZoneSensor[" + self.id + "]: zone=" + self.zone
        print("getStatus() —", msg)
        return msg


class EnvSensor(Thing):
    def __init__(self, thing_id, name, temperature, light_lux):
        super().__init__(thing_id, name)
        self.temperature = temperature
        self.lightLux = light_lux

    def getStatus(self):
        msg = (
            "EnvSensor["
            + self.id
            + "]: temperature="
            + str(round(self.temperature, 1))
            + "°C, lightLux="
            + str(int(self.lightLux))
        )
        print("getStatus() —", msg)
        return msg


class Scoreboard(Thing):
    def __init__(self, thing_id, name, score_a=0, score_b=0, timer_sec=0):
        super().__init__(thing_id, name)
        self.scoreA = score_a
        self.scoreB = score_b
        self.timerSec = timer_sec

    def show(self):
        print(
            "show() — табло:",
            self.name,
            "|",
            self.scoreA,
            ":",
            self.scoreB,
            "| таймер",
            self.timerSec,
            "с",
        )

    def getStatus(self):
        msg = (
            "Scoreboard["
            + self.id
            + "]: "
            + str(self.scoreA)
            + ":"
            + str(self.scoreB)
            + ", timer="
            + str(self.timerSec)
            + "s"
        )
        print("getStatus() —", msg)
        return msg


class CourtDataStore:
    def __init__(self):
        self.events = []
        self.telemetry = []

    def saveEvent(self, data):
        line = "event=" + repr(data)
        self.events.append(line)
        print("saveEvent(", data, ")")

    def saveTelemetry(self, data):
        line = "telemetry=" + repr(data)
        self.telemetry.append(line)
        print("saveTelemetry(", data, ")")

    def getRecords(self):
        all_records = self.events + self.telemetry
        print("getRecords() — записей:", len(all_records))
        return all_records


class MainControlUnit:
    def __init__(self, things, store, scoreboard):
        self.things = things
        self.store = store
        self.scoreboard = scoreboard

    def collectData(self):
        print("collectData() — опрос устройств:", len(self.things))
        for t in self.things:
            status = t.getStatus()
            self.store.saveTelemetry({"id": t.id, "status": status})

    def calculateScore(self):
        print("calculateScore() — пересчёт счёта")
        basket_scored = False
        for t in self.things:
            if isinstance(t, ScoreSensor) and t.is_goal:
                basket_scored = True
                break
        if basket_scored:
            self.scoreboard.scoreA = self.scoreboard.scoreA + 1
            self.store.saveEvent({"type": "basket", "points": self.scoreboard.scoreA})

    def updateScoreboard(self):
        print("updateScoreboard() — обновление табло")
        self.scoreboard.timerSec = self.scoreboard.timerSec + 1
        self.scoreboard.show()
