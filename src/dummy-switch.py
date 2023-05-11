import paho.mqtt.client as mqtt
import threading
from time import sleep
import sys
import argparse as ag

topic = "redes2/2321/02/"
broker_address = "localhost"
broker_port = 1883
probability = 0.3


class interruptor:
    def __init__(self, id) -> None:
        self.state = "OFF"
        self.id = id
        self.client = mqtt.Client()

    def connect(self):
        try:
            self.client.connect(broker_address, broker_port)
            self.new_topic = topic+str(self.id)
            self.client.subscribe(self.new_topic+"write")
            return 1
        except:
            return -1

    def on_response(self, user, userdate, message):
        msg = message.payload.decode()
        print(msg)
        if msg == "on":
            self.state = "ON"
        elif msg == "off":
            self.state = "OFF"

    def publish(self):
        while True:
            self.client.publish(self.new_topic+"read", "" +
                                str(self.id)+":estado:"+self.state)
            sleep(1)


if __name__ == "__main__":
    argumentsparsed = ag.ArgumentParser()
    argumentsparsed.add_argument("--host", help="hostanem", type=str)
    argumentsparsed.add_argument("--port", "--p", help="port number", type=int)
    argumentsparsed.add_argument("-P", "--probability", help="probability", type=float)
    argumentsparsed.add_argument(
    "required_arg", help="id", type=int)
    args = argumentsparsed.parse_args()
    if (args.port):
        broker_port = args.port
    if (args.host):
        broker_address = args.host
    if (args.probability):
        probability = args.probability

    print(broker_address)
    print(broker_port)
    print(probability)
    interr = interruptor(args.required_arg)
    if interr.connect() != 1:
        print("Error al conectarse al broker")
        sys.exit(0)
    interr.client.on_message = interr.on_response
    hilo1 = threading.Thread(target=interr.publish)
    hilo1.start()
    interr.client.loop_forever()
