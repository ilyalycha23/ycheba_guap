"""
Классы Thing и Sensor - валидация данных (try-except)
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
        except ValueError as e:
            print(f'New value has not accept, need number (1, 2 or 3) but given: {request.args.get("value", "")}')
            return json.dumps({"power": "error", "message": str(e)})
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({"power": self.power})
