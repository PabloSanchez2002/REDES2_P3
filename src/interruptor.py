import paho.mqtt.client as mqtt
import threading
from time import sleep

topic = "redes2/2321/02/"
broker_address = "localhost"
broker_port = 1883
class interruptor:
    def __init__(self) -> None:
        self.state = "OFF"
        self.id = input("Introduce el id del interruptor: ")
        self.client = mqtt.Client()
        self.client.connect(broker_address, broker_port)
        self.new_topic = topic+str(self.id)
        self.client.subscribe(self.new_topic+"write")

    def on_response(self, user, userdate, message):
        msg = message.payload.decode()
        print (msg)
        if msg == "on":
            self.state = "ON"
        elif msg == "off":
            self.state = "OFF"

    def publish(self):
        while True:
            self.client.publish(self.new_topic+"read", ""+str(self.id)+":estado:"+self.state)
            sleep(5)


if __name__ == "__main__":
    interr = interruptor()
    interr.client.on_message = interr.on_response
    hilo1 = threading.Thread(target=interr.publish)
    hilo1.start()
    interr.client.loop_forever()

