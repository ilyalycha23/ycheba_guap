"""
Классы Thing и Sensor - приём данных от внешних источников
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
    """Датчик попаданий - принимает очки извне (ввод пользователя)"""
    
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        self.power = "on"
        print('sensor has create')
    
    def connect(self, request):
        super().connect()
        self.value = request.args.get('value', '')
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({"power": self.power})
