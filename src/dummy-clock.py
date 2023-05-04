import datetime
import paho.mqtt.client as mqtt
from time import sleep

topic = "redes2/2321/02/"
broker_address = "localhost"
broker_port = 1883


class reloj:

    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.id = int(input("Introduce el id del reloj: "))
        self.client.connect(broker_address, broker_port)
        self.new_topic = topic+str(self.id)
        self.client.subscribe(self.new_topic)
   
    def publish(self):
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.hora = self.hora.replace(":","-")
        self.client.publish(self.new_topic, ""+str(self.id)+":hora:"+self.hora)
    
if __name__ == "__main__":
    sens = reloj()
    while True:
        sens.publish()
        sleep(10)