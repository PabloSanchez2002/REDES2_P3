import paho.mqtt.client as mqtt
import argparse as ag
import json

broker_address = "localhost"
broker_port = 1883
topic = "redes2/2321/02/rule"
client = mqtt.Client()


class rule_engine:
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.new_topic = topic
        self.client.connect(broker_address, broker_port)
        self.client.subscribe(self.new_topic+"write")

    def publish(self):
        self.client.publish(self.new_topic, "1:rule:OFF")

    def on_response(self, client, userdate, message):
        tupla = json.loads(message.payload.decode())
        print(tupla)

        datos = tupla[0]
        reglas = tupla[1]
        for regla in reglas:
            try:
                regla = regla.split(":")
                dato = datos[regla[0]]
                if regla[1] == "=":
                    if int(dato) == int(regla[2]):
                        self.client.publish(
                            self.new_topic+"read", regla[3]+":rule:"+regla[4])

                elif regla[1] == ">":
                    if int(dato) > int(regla[2]):
                        self.client.publish(
                            self.new_topic+"read", regla[3]+":rule:"+regla[4])

                elif regla[1] == "<":
                    if int(dato) < int(regla[2]):
                        self.client.publish(
                            self.new_topic+"read", regla[3]+":rule:"+regla[4])
            except:
                pass


if __name__ == "__main__":
    argumentsparsed = ag.ArgumentParser()
    argumentsparsed.add_argument("--host", help="hostanem", type=str)
    argumentsparsed.add_argument(
        "--port", "--p", help="port number", type=int)
    args = argumentsparsed.parse_args()
    if (args.port):
        broker_port = args.port
    if (args.host):
        broker_address = args.host
    rule_eng = rule_engine()
    rule_eng.client.on_message =rule_eng.on_response
    rule_eng.client.loop_forever()
    