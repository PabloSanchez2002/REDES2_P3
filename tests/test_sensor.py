
"""
Ejecutar un sensor, 
python3 src/dummy-sensor.py 1
Ejecutar este programa:
python3 tests/test-sensor.py 1

En test-sensor.py debería de ir apareciendo los valores de la temperatura que varían en el intervalo expuesto
"""

import sys
import paho.mqtt.client as mqtt
import argparse as ag
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
            self.client.subscribe(self.new_topic)
            self.client.on_message = self.on_rule_message
            return 1
        except:
            return -1

if __name__ == "__main__":

    argumentsparsed = ag.ArgumentParser()
    argumentsparsed.add_argument(
    "required_arg", help="id", type=int)
    args = argumentsparsed.parse_args()
 
    test = tester(args.required_arg)
    if test.connect() != 1:
        print("Error al conectarse al broker")
        sys.exit(0)
    
    test.client.loop_forever()
    