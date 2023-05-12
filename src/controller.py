import os
import paho.mqtt.client as mqtt
import threading
import sys
import json
from time import sleep
import argparse as ag

broker_address = "localhost"
broker_port = 1883
topic = "redes2/2321/02/"

class Controlador:
    
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.client.connect(broker_address, broker_port)
        self.client.subscribe(topic+"ruleread")
        self.client.subscribe(topic+"bridge_send")
        self.send_topic = topic + "bridge_receive"
        self.client.on_message = self.on_rule_message

        self.dict_topics= {}     #id:topic
        self.array_reglas = []   #reglas
        self.valores = {}        #id:(magnitud:valor)
        self.valores_rule = {}   #magnitud:valor
        try:
            self.load_data()
            for topical in self.dict_topics.keys():
                self.client.subscribe(self.dict_topics[topical].replace("write", "read"))
                print(self.dict_topics)
        except:
            pass
        hilo = threading.Thread(target=self.rule_engine)
        hilo.start()
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            self.save_data()


    def on_rule_message(self, client, userdata, message):
        # "<id>:<parametro>:<datos>"
        tokens = message.payload.decode().split(":")
        print(tokens)
        #try:
        if (tokens[0] == "bridge"):
            if (tokens[1] == "newsensor"):
                self.create_sensor(tokens[2])
            elif (tokens[1] == "newactuador"):
                print("AAAAAAAAaa")
                self.create_actuador(tokens[2])
            elif (tokens[1] == "newrule"):
                self.create_regla(
                    tokens[2], tokens[3], tokens[4], tokens[5], tokens[6])
            elif (tokens[1] == "get"):
                try:
                    print("bridge solicita dato:" + self.valores[tokens[2]])
                    self.client.publish(self.send_topic, self.valores[tokens[2]])
                except:
                    pass

        elif (tokens[1] == "rule"):
            try:
                print(self.dict_topics[tokens[0]])
                client.publish(self.dict_topics[tokens[0]], tokens[2]) 
            except:
                pass
        
        else:
            self.valores[tokens[0]] = tokens[1]+":"+tokens[2]
            # Actualiza en el caso de que llegue un dato nuevo
            self.valores_rule[tokens[1]] = tokens[2]
            print(self.valores)
            print(self.valores_rule)
        #except:
        #    pass

    def create_sensor(self, id):
        new_topic = topic+str(id)
        self.dict_topics[id] = new_topic
        self.client.subscribe(new_topic)
        print(self.dict_topics)

    def create_actuador(self, id):
        new_topic = topic+str(id)
        self.dict_topics[id] = new_topic+"write"
        self.client.subscribe(new_topic+"read")
        print(self.dict_topics)
        
    def create_regla(self, magnitud, operador, valor, id_actuador, accion):
        str = ""+magnitud + ":" + operador + ":" + valor + ":" + id_actuador + ":" + accion
        self.array_reglas.append(str)
        


    def rule_engine(self):
        while True:
            self.client.publish(topic+"rulewrite", json.dumps((self.valores_rule, self.array_reglas))) 
            sleep(1)

    def save_data(self):
        save = [self.dict_topics, self.array_reglas]
        with open('data.json', 'w') as f:
            json.dump(save, f)

    def load_data(self):
        load = []
        with open('data.json', 'r') as f:
            load = json.load(f)
        self.dict_topics = dict(load[0])
        self.array_reglas = load[1]
        

if __name__ == '__main__':
    try:
        argumentsparsed = ag.ArgumentParser()
        argumentsparsed.add_argument("--host", help="hostanem", type=str)
        argumentsparsed.add_argument("--port", "--p", help="port number", type=int)
        args = argumentsparsed.parse_args()
        if (args.port):
            broker_port = args.port
        if (args.host):
            broker_address = args.host
        control = Controlador()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)




