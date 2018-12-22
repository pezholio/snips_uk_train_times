#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from nredarwin.webservice import DarwinLdbSession

import io

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class TrainTimes(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None
        
        api_key = self.config.get("secret").get("nre_api_key")
        
        self.home_station_code = self.config.get("secret").get("home_station_code")
        self.darwin = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=api_key)

        # start listening to MQTT
        self.start_blocking()
        
    # --> Sub callback function, one per intent
    def train_to_callback(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        
        depature = self.next_departure_to_station('BHM')
        time = depature.std
        
        output = "The next train to Birmingham New Street is the %s" % (time)
                                                                              
        print output

        # if need to speak the execution result by tts
        hermes.publish_end_session(intent_message.session_id, output)
    
    def next_departure_to_station(station_code):
        board = self.darwin.get_station_board(self.home_station_code)
        s = None
        for service in board.train_services:
            service_detail = darwin.get_service_details(service.service_id)
            codes = map(lambda x: x.crs, service_detail.subsequent_calling_points)
            if station_code in codes:
                s = service
                break
        return s
        
    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.train_to_callback).start()

if __name__ == "__main__":
    TrainTimes()
