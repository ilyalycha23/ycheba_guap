"""
Классы Thing, Sensor, Scoreboard и Logger
"""
import abc
import pymongo
import datetime


class Thing(abc.ABC):
    """Абстрактный базовый класс для IoT-объектов"""
    
    def __init__(self, name):
        self.name = name
        print('create Thing')
    
    @abc.abstractmethod
    def connect(self, *args):
        print('Connection start')


class Sensor(Thing):
    """Датчик попаданий"""
    
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
    """Табло счёта - актуатор"""
    
    def __init__(self, name, score_threshold):
        super().__init__(name)
        self.power = 'Off'
        self.total_score = 0
        self.score_threshold = score_threshold
    
    def connect(self):
        super().connect()
        return {"scoreboard_power": self.power}
    
    def auto_display(self, points):
        self.total_score += points
        self.power = 'On' if self.total_score >= self.score_threshold else 'Off'


class Logger:
    """Логгер - сохранение и получение данных из MongoDB"""
    
    def __init__(self, db_name):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
    
    def insert_score(self, new_data):
        """Сохраняет очки в БД при каждом попадании"""
        return self.db['Scores'].insert_one({
            'timeStamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Points': new_data
        })
    
    def get_all_scores(self):
        """Получение всех записей из коллекции Scores"""
        records = list(self.db['Scores'].find({}, {'_id': 0}))
        return records
