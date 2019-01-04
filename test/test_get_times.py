import re

from nredarwin.webservice import DarwinLdbSession
from .. import get_times

class TestGetTimes(object):
    
    def darwin_session(self):
        return DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key='55ede721-e99e-488b-9087-bcfb611f54f3')
    
    def test_gets_times(self):
        times = get_times.GetTimes(self.darwin_session(), 'BKT', 'BHM')
        assert re.match('The next train to Birmingham New Street is the', times.response())
    
    def test_returns_error(self):
        times = get_times.GetTimes(self.darwin_session(), 'BKT', 'XXX')
        assert re.match("Sorry, I couldn't find any departures for your stations", times.response())
    
    def test_gets_station_name(self):
        times = get_times.GetTimes(self.darwin_session(), 'BKT', 'BHM')
        assert times.station_name('BHM') == 'Birmingham New Street'
