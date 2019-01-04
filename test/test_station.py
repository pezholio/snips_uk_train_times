from .. import station

class TestStations(object):
    
    def test_can_be_inititalized(self):
        s = station.Station('ABC', 'Station')
        assert s.code == 'ABC'
        assert s.name == 'Station'
    
    def test_gets_all(self):
        stations = station.Station.all()
        assert len(stations) == 2570
    
    def test_gets_station_by_code(self):
        s = station.Station.find_by_code('BHM')
        assert s.name == 'Birmingham New Street'
        assert s.code == 'BHM'

    def returns_none(self):
        s = station.Station.find_by_code('XXX')
        assert s == None
    
    def test_gets_station_by_name(self):
        s = station.Station.find_by_name('Birmingham New Street')
        assert s.name == 'Birmingham New Street'
        assert s.code == 'BHM'
