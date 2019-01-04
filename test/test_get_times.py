import re
import vcr

from nredarwin.webservice import DarwinLdbSession
from .. import get_times

class TestGetTimes(object):
    
    def darwin_session(self):
        return DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key='55ede721-e99e-488b-9087-bcfb611f54f3')
    
    @vcr.use_cassette('fixtures/vcr_cassettes/gets_times.yaml', record_mode='new_episodes')
    def test_gets_times(self):
        times = get_times.GetTimes(self.darwin_session(), 'BKT', 'BHM')
        assert times.response() == 'The next train to Birmingham New Street is the 13:52'
    
    @vcr.use_cassette('fixtures/vcr_cassettes/returns_error.yaml', record_mode='new_episodes')
    def test_returns_error(self):
        times = get_times.GetTimes(self.darwin_session(), 'BKT', 'XXX')
        assert times.response() == "Sorry, I couldn't find any departures for your stations"
    
    @vcr.use_cassette('fixtures/vcr_cassettes/with_delay.yaml', record_mode='new_episodes')
    def test_with_delay(self):
        times = get_times.GetTimes(self.darwin_session(), 'BKT', 'BHM')
        assert times.response() == 'The next train to Birmingham New Street is the 13:52, expected to depart at 13:55'
