import os
import sys
import threading
import asyncio
import discord
import paho.mqtt.client as mqtt
import argparse as ag
from multiprocessing import Queue
import time
import signal
import os


token = "MTEwMDcxODE2MDI3NTA2Njg5MA.GSkF9C.MY1kNb6gpBPOtmoTTqyeovZ82iS8NTbLH6AwCc"
channel_id = 1100705328078782507
broker_address = "localhost"
broker_port = 1883
topic = "redes2/2321/02/"


class Bridge:
    def __init__(self) -> None:

        self.client = mqtt.Client()
        self.client.connect(broker_address, broker_port)
        self.receive_topic = topic+"bridge_receive"
        self.send_topic = topic+"bridge_send"
        self.client.subscribe(self.receive_topic)
        self.client.on_message = self.on_rule_message

        self.answer_queue = Queue()

        self.sem = threading.Semaphore(0)
        #self.loop = asyncio.new_event_loop()

        hilo = threading.Thread(target=self.run_bot).start()
        hilo1 = threading.Thread(target=self.responder).start()
       
        
        self.client.loop_forever()
        

    def run_bot(self):
        intents = discord.Intents.all()
        intents.members = True

        self.discord_client = discord.Client(intents=intents)

        @self.discord_client.event
        async def on_ready():
            print('Bot de Discord conectado como {0.user}'.format(
                self.discord_client))
            #for chann in self.discord_client.get_all_channels():
            #    print(str(chann.id) + "  " + chann.name)
            #    if str(chann.id) == channel_id:
            #        CHANNEL = chann
            #        print(chann.type)


        @self.discord_client.event
        async def on_message(message):
            if message.author == self.discord_client.user:
                return

            else:
                # try:
                message.content = message.content.lower()
                tokens = message.content.split(" ")
                if tokens[0] == "añadir":
                    print("entra en añadir")
                    if tokens[1] == "sensor":
                        self.client.publish(
                            self.send_topic, "bridge:newsensor:" + tokens[2])
                        
                    elif tokens[1] == "actuador":
                        self.client.publish(
                            self.send_topic, "bridge:newactuador:" + tokens[2])

                    elif tokens[1] == "regla":
                        self.client.publish(
                            self.send_topic, "bridge:newrule:" + str(tokens[2]) + ":" + str(tokens[3]) + ":" + str(tokens[4]) + ":" + str(tokens[5]) + ":" + str(tokens[6]))

                elif tokens[0] == "obtener":
                    print("entra en obtener:" + self.send_topic)
                    self.client.publish(
                        self.send_topic, "bridge:get:" + str(tokens[1]))

                else:
                    print("El comando que has introducido no es valido.")

                # except:
                #    print("El comando que has introducido no funcionó.")


        try:
            self.discord_client.run(token)
        except:
            return

    def on_rule_message(self, client, userdata, msg):
        print("me llega algo! ->" + str(msg.payload.decode()))
        if msg.topic == self.receive_topic:
            self.answer_queue.put(msg.payload.decode())
            self.sem.release()
           

    def responder(self):
        while(True):
            self.sem.acquire()
            temp = self.answer_queue.get(block=True)
            task = asyncio.run_coroutine_threadsafe(self.enviar(temp), self.discord_client.loop)
            task.result()


    async def enviar(self, message):
        channel = self.discord_client.get_channel(channel_id)
        await channel.send(message)

def main():
    """Punto de entrada de ejecución
    """
    bot = Bridge()


if __name__ == '__main__':
    try:
        argumentsparsed = ag.ArgumentParser()
        argumentsparsed.add_argument("--host", help="hostanem", type=str)
        argumentsparsed.add_argument(
            "--port", "--p", help="port number", type=int)
        args = argumentsparsed.parse_args()
        if (args.port):
            broker_port = args.port
        if (args.host):
            broker_address = args.host
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
