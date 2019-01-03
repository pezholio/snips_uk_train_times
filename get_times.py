from nredarwin.webservice import DarwinLdbSession

class GetTimes:
    def __init__(self, api_key, home, to):
        self.darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=api_key)
        self.home = home
        self.to = to
    
    def response(self):
        departure = self.next_departure()
        
        if (departure != None):
            time = departure.std
            return "The next train is the %s" % (time)
        else:
            return "Sorry, I couldn't find any departures for your stations"
    
    def next_departure(self):
        board = self.darwin.get_station_board(self.home)
        s = None
        for service in board.train_services:
            service_detail = self.darwin.get_service_details(service.service_id)
            codes = map(lambda x: x.crs, service_detail.subsequent_calling_points)
            if self.to in codes:
                s = service
                break
        return s