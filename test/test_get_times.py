import re
from .. import get_times

class TestGetTimes(object):
    
    def api_key(self):
        return '55ede721-e99e-488b-9087-bcfb611f54f3'
    
    def test_gets_times(self):
        times = get_times.GetTimes(self.api_key(), 'BKT', 'BHM')
        assert re.match('The next train is the', times.response())
    
    def test_returns_error(self):
        times = get_times.GetTimes(self.api_key(), 'BKT', 'XXX')
        assert re.match("Sorry, I couldn't find any departures for your stations", times.response())
