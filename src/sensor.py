import random
import paho.mqtt.client as mqtt


topic = "redes2/2321/02/"
broker_address = "localhost"
broker_port = 1883

class sensor:
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.id = int(input("Introduce el id del sensor: "))
        self.client.connect(broker_address, broker_port)
        self.new_topic = topic+str(self.id)
        self.client.subscribe(self.new_topic)
        
    def publish(self):
        self.temperatura = random.randint(10,30)
        self.client.publish(self.new_topic, ""+str(self.id)+":temperatura:"+str(self.temperatura))

if __name__ == "__main__":
    sens = sensor()
    sens.publish()