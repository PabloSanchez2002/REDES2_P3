
"""
    Ejecutar tests/test_switch.py 1
    Ejecutar src/dummy-switch.py 1 

    En test_switch se irán viendo los estados y como cada 5 segundos el estado cambia a !estado

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
            self.new_topic = topic+str(self.id)
            self.client.subscribe(self.new_topic+"read")
            self.client.on_message = self.on_rule_message
            return 1
        except:
            return -1
    def publish(self):
        var = "off"
        while True: 
            self.client.publish(self.new_topic+"write", var)
            if var == "off":
                var = "on"
            else:
                var = "off"
            sleep(5)
if __name__ == "__main__":

    argumentsparsed = ag.ArgumentParser()
    argumentsparsed.add_argument(
    "required_arg", help="id", type=int)
    args = argumentsparsed.parse_args()
 
    test = tester(args.required_arg)
    if test.connect() != 1:
        print("Error al conectarse al broker")
        sys.exit(0)

    hilo = threading.Thread(target=test.publish)
    hilo.start()
    test.client.loop_forever()
    