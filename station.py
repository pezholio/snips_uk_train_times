import csv

class Station:
    @classmethod
    def all(cls):
        stations = []
        with open('station_codes.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                stations.append(cls(row[0], row[1]))
        return stations
    
    @classmethod
    def find_by_code(cls, code):
        return cls.find(lambda s: s.code == code)
    
    @classmethod
    def find_by_name(cls, name):
        return cls.find(lambda s: s.name == name)
    
    @classmethod
    def find(cls, f):
        station_list = filter(f, cls.all())
        return next(iter(station_list), None)
    
    def __init__(self, code, name):
        self.code = code
        self.name = name
