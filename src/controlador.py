import discord
import paho.mqtt.client as mqtt
import threading
import sys
import json
from time import sleep
client = mqtt.Client()

token = "MTEwMDcxODE2MDI3NTA2Njg5MA.GSkF9C.MY1kNb6gpBPOtmoTTqyeovZ82iS8NTbLH6AwCc"

broker_address = "localhost"
broker_port = 1883
topic = "redes2/2321/02/"

client.connect(broker_address, broker_port)
client.subscribe(topic+"ruleread")

dict_topics= {}     #id:topic
array_reglas = []   #reglas
valores = {}        #id:(magnitud:valor)
valores_rule = {}   #magnitud:valor


def on_rule_message(client, userdata, message):
    # "<id>:<parametro>:<datos>"
    tokens = message.payload.decode().split(":")
    try:
        if (tokens[1] == "rule"):
            client.publish(dict_topics[int(tokens[0])], tokens[2]) 
            
        else:
            valores[tokens[0]] = tokens[1]+":"+tokens[2]
            valores_rule[tokens[1]] = tokens[2] #Actualiza en el caso de que llegue un dato nuevo
            print(valores)
            print(valores_rule)
    except:
        pass

def create_sensor(id):
    new_topic = topic+str(id)
    dict_topics[id] = new_topic
    client.subscribe(new_topic)
    print(dict_topics)

def create_actuador(id):
    new_topic = topic+str(id)
    dict_topics[id] = new_topic+"write"
    client.subscribe(new_topic+"read")
    print(dict_topics)
    
def create_regla(magnitud, operador, valor, id_actuador, accion):
    str = ""+magnitud + ":" + operador + ":" + valor + ":" + id_actuador + ":" + accion
    array_reglas.append(str)
    

def interruptor_send():
    pass

client.on_message = on_rule_message

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
                    if tokens[1] == "actuador":
                        create_actuador(int(tokens[2]))
                        
                    elif tokens[1] == "regla":
                        create_regla(tokens[2], tokens[3],
                                     tokens[4], tokens[5], tokens[6])

                elif tokens[0] == "obtener":
                    mensaje = valores[tokens[1]]
                    await message.channel.send(mensaje.format(message))

                else:
                    print("El comando que has introducido no es valido.")
                    
            except:
                print("El comando que has introducido no es valido.")
    try:
        discord_client.run(token)
    except:
        return

def rule_engine():
    while True:
        client.publish(topic+"rulewrite", json.dumps((valores_rule, array_reglas))) 
        sleep(5)

hilo1 = threading.Thread(target=discord_run)
hilo1.start()

hilo2 = threading.Thread(target=rule_engine)
hilo2.start()

client.loop_forever()
