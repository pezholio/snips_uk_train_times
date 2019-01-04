#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from nredarwin.webservice import DarwinLdbSession
from get_times import GetTimes

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
        self.destination_code = self.config.get("secret").get("destination_code")
        self.darwin_session = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=api_key)

        # start listening to MQTT
        self.start_blocking()
        
    # --> Sub callback function, one per intent
    def train_to_callback(self, hermes, intent_message):
        if intent_message.intent.intent_name == 'pezholio:next_departure':
            print '[Received] intent: {}'.format(intent_message.intent.intent_name)
            
            get_times = GetTimes(self.darwin_session, self.home_station_code, self.destination_code)
                                                                                      
            # if need to speak the execution result by tts
            hermes.publish_end_session(intent_message.session_id, get_times.response())
        else:
            return
    
        
    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.train_to_callback).start()

if __name__ == "__main__":
    TrainTimes()
