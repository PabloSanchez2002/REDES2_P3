import datetime
import paho.mqtt.client as mqtt
from time import sleep
import argparse as ag

topic = "redes2/2321/02/"
broker_address = "localhost"
broker_port = 1883
increment = 1
rate = 1


class reloj:

    def __init__(self, id) -> None:
        self.client = mqtt.Client()
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.id = id
        self.client.connect(broker_address, broker_port)
        self.new_topic = topic+str(self.id)
        self.client.subscribe(self.new_topic)
   
    def publish(self):
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.hora = self.hora.replace(":","-")
        self.client.publish(self.new_topic, ""+str(self.id)+":hora:"+self.hora)
    
if __name__ == "__main__":
    argumentsparsed = ag.ArgumentParser()
    argumentsparsed.add_argument("--host", help="hostanem", type=str)
    argumentsparsed.add_argument("--port", "--p", help="port number", type=int)
    argumentsparsed.add_argument( "--increment", help="increment", type=int)
    argumentsparsed.add_argument( "--rate", help="rate", type=int)
    argumentsparsed.add_argument(
    "required_arg", help="id", type=int)
    args = argumentsparsed.parse_args()
    if (args.port):
        broker_port = args.port
    if (args.host):
        broker_address = args.host
    if (args.increment):
        increment = args.increment
    if (args.increment):
        rate = args.rate
    sens = reloj(args.required_arg)
    while True:
        sens.publish()
        sleep(10)