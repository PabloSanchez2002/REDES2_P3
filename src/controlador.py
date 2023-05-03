import discord
import asyncio
import paho.mqtt.client as mqtt
import threading
import sys
import subprocess

client = mqtt.Client()


token = "MTEwMDcxODE2MDI3NTA2Njg5MA.GSkF9C.MY1kNb6gpBPOtmoTTqyeovZ82iS8NTbLH6AwCc"

broker_address = "localhost"
broker_port = 1883
topic = "redes2/2321/02/"
client.connect(broker_address, broker_port)
dict_topics= {}
array_reglas = []
valores = {}
valores_rule = {}


def on_rule_message(client, userdata, message):
    # "<id>:<parametro>:<datos>"
    tokens = message.payload.decode().split(":")
    valores[tokens[0]] = tokens[1]+":"+tokens[2]
    valores_rule[tokens[1]] = tokens[2]
    print(valores)
    print(valores_rule)
    sys.stdout.flush()

client.on_message = on_rule_message
def create_sensor(id):
    new_topic = topic+str(id)
    dict_topics[id] = new_topic
    client.subscribe(new_topic)
    print(dict_topics)
    

def create_actuador(id):
    new_topic = topic+str(id)
    dict_topics[id] = new_topic
    client.subscribe(new_topic)

def interruptor_send():
    pass

def discord_run():
    intents = discord.Intents.all()
    intents.members = True

    discord_client = discord.Client(intents=intents)


    @discord_client.event
    async def on_ready():
        print('Bot de Discord conectado como {0.user}'.format(discord_client))


    @discord_client.event
    async def on_message(message):
        if message.author == discord_client.user:
            return

        else:
            try:
                message.content = message.content.lower()
                tokens = message.content.split(" ")
                if tokens[0] == "añadir":
                    if tokens[1] == "sensor":
                        create_sensor(int(tokens[2]))
                    elif tokens[1] == "actuador":
                        create_actuador(int(tokens[2]))
                    elif tokens[1] == "regla":
                        pass

                elif tokens[0] == "obtener":
                    pass

                else:
                    print("El comando que has introducido no es valido.")
                    
            except:
                print("El comando que has introducido no es valido.")
    discord_client.run(token)


hilo = threading.Thread(target=discord_run)
hilo.start()
client.loop_forever()
