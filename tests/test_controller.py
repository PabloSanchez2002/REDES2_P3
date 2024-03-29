

"""
    Ejecutar en el orden puesto aqui:
    python3 src/controller.py
    python3 tests/test_controller.py 1
    python3 src/dummy-switch.py 2

    En controller.py veremos el estado del switch
    En dummy-switch veremos como cada 10s cambia el estado
"""

import sys
import paho.mqtt.client as mqtt
import argparse as ag
from time import sleep
import threading

topic = "redes2/2321/02/"
broker_address = "localhost"
broker_port = 1883
max = 30
min = 20
interval = 1
increment = 1

class tester:
    def __init__(self, id) -> None:
        self.client = mqtt.Client()
        self.id = id

    def on_rule_message(self, client, userdata, message):
        tokens = message.payload.decode().split(":")
        print(tokens)
       
    def connect(self):
        try:
            self.client.connect(broker_address, broker_port)
            self.topic_sensor = topic+str(self.id)
            self.topic_rule = topic+"ruleread"
            self.send_topic = topic + "bridge_send"
            self.client.on_message = self.on_rule_message
            return 1
        except:
            return -1
    def publish(self):
        self.client.publish(self.send_topic, "bridge:newactuador:2")
        self.client.publish(self.send_topic, "bridge:newsensor:1")
        self.client.publish(self.topic_sensor, "1:temperatura:20")
        while True: 
            sleep(10)
            self.client.publish(self.topic_rule, "2:rule:on")
            sleep(10)
            self.client.publish(self.topic_rule, "2:rule:off")
            sleep(10)

if __name__ == "__main__":

    argumentsparsed = ag.ArgumentParser()
    argumentsparsed.add_argument(
    "required_arg", help="id", type=int)
    args = argumentsparsed.parse_args()
 
    test = tester(args.required_arg)
    if test.connect() != 1:
        print("Error al conectarse al broker")
        sys.exit(0)

    test.publish()
    