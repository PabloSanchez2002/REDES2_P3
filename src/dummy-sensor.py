import random
import paho.mqtt.client as mqtt
from time import sleep
import argparse as ag


topic = "redes2/2321/02/"
broker_address = "localhost"
broker_port = 1883
max = 30
min = 20
interval = 1
increment = 1

class sensor:
    def __init__(self, id) -> None:
        self.client = mqtt.Client()
        self.id = id
        self.client.connect(broker_address, broker_port)
        self.new_topic = topic+str(self.id)
        self.client.subscribe(self.new_topic)
        self.temperatura = min
        
    def publish(self):
        self.temperatura = self.temperatura + increment
        if (self.temperatura > max):
            self.temperatura = min
        self.client.publish(self.new_topic, ""+str(self.id)+":temperatura:"+str(self.temperatura))

if __name__ == "__main__":
    argumentsparsed = ag.ArgumentParser()
    argumentsparsed.add_argument("--host", help="hostanem", type=str)
    argumentsparsed.add_argument("--port", "--p", help="port number", type=int)
    argumentsparsed.add_argument("-M", "--max", help="max", type=int)
    argumentsparsed.add_argument("-m", "--min", help="min", type=int)
    argumentsparsed.add_argument("-i", "--interval", help="interval", type=int)
    argumentsparsed.add_argument( "--increment", help="increment", type=int)
    argumentsparsed.add_argument(
    "required_arg", help="id", type=int)
    args = argumentsparsed.parse_args()
    if (args.port):
        broker_port = args.port
    if (args.host):
        broker_address = args.host
    if (args.max):
        max = args.max
    if(args.min):
        min = args.min
    if(args.interval):
        interval = args.interval
    if (args.increment):
        increment = args.increment
    sens = sensor(args.required_arg)
    while True:
        sens.publish()
        sleep(interval)