import csv

class GetTimes:
    def __init__(self, darwin_session, home, to):
        self.darwin = darwin_session
        self.home = home
        self.to = to
    
    def response(self):
        departure = self.next_departure()
        
        if (departure != None):
            time = departure.std
            return "The next train to %s is the %s" % (self.station_name(self.to), time)
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
    
    def station_name(self, code):
        return self.station_dict()[code]

    def station_dict(self):
        with open('station_codes.csv') as f:
           d = dict(filter(None, csv.reader(f)))
        return d
