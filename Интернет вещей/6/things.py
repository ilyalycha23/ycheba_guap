"""
Классы Thing, Sensor и Scoreboard (интеллектуальный актуатор)
"""
import abc
import json


class Thing(abc.ABC):
    """Абстрактный базовый класс для IoT-объектов"""
    
    def __init__(self, name):
        self.name = name
        print('create Thing')
    
    @abc.abstractmethod
    def connect(self, *args):
        print('Connection start')


class Sensor(Thing):
    """Датчик попаданий - валидация: только 1, 2 или 3 очка"""
    
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        self.power = "on"
        print('sensor has create')
    
    def connect(self, request):
        super().connect()
        try:
            val = request.args.get('value', '')
            float(val)
            self.value = int(val)
            if self.value not in [1, 2, 3]:
                raise ValueError('Очки должны быть 1, 2 или 3')
        except ValueError:
            print(f'New value has not accept, need number (1, 2 or 3) but given: {request.args.get("value", "")}')
            return {"power": "error"}
        print(f'Connection with {self.name} success, new value is {self.value}')
        return {"power": self.power}


class Scoreboard(Thing):
    """Табло счёта - актуатор. Подсветка при наборе порога очков."""
    
    def __init__(self, name, score_threshold):
        super().__init__(name)
        self.power = 'Off'
        self.total_score = 0
        self.score_threshold = score_threshold  # порог для включения подсветки
    
    def connect(self):
        super().connect()
        return {"scoreboard_power": self.power}
    
    def auto_display(self, points):
        """Обновляет счёт и включает подсветку при достижении порога"""
        self.total_score += points
        self.power = 'On' if self.total_score >= self.score_threshold else 'Off'
