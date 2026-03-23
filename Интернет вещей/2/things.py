"""
Классы Thing и Sensor для IoT-системы умного баскетбольного поля
"""
import abc
import json
import random


class Thing(abc.ABC):
    """Абстрактный базовый класс для IoT-объектов"""
    
    def __init__(self, name):
        self.name = name
        print('create Thing')
    
    @abc.abstractmethod
    def connect(self, *args):
        print('Connection start')


class Sensor(Thing):
    """Датчик попаданий мяча в корзину (очки за бросок)"""
    
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit  # 'points' - очки
        self.value = 0
        print('sensor has create')
    
    def connect(self):
        super().connect()
        self.emulate()
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})
    
    def emulate(self):
        """Эмуляция: случайное попадание 1, 2 или 3 очка"""
        self.value = random.choice([1, 2, 3])
