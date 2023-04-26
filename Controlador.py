import discord
import asyncio
import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client()

token = "MTEwMDcxODE2MDI3NTA2Njg5MA.GSkF9C.MY1kNb6gpBPOtmoTTqyeovZ82iS8NTbLH6AwCc"


# Configurar el cliente MQTT
mqtt_client.username_pw_set("username", "password")
mqtt_client.connect("localhost", 1883)

intents = discord.Intents.all()
intents.members = True

# Crear una instancia del cliente de Discord con los intents habilitados
discord_client = discord.Client(intents=intents)

# Definir una función para manejar la conexión del bot de Discord


@discord_client.event
async def on_ready():
    print('Bot de Discord conectado como {0.user}'.format(discord_client))


# Definir una función para manejar los mensajes del bot de Discord
@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    elif message.content.startswith('!mqtt '):
        print("Mensaje mqtt: " + message.content)
        #mqtt_topic = message.content[6:]
        #mqtt_payload = "Hello, world!"
        #mqtt_client.publish(mqtt_topic, mqtt_payload)
        #await message.channel.send('Mensaje enviado a MQTT')

    else:
        print("Este mensaje no ses mqtt: " + message.content)

# Conectar el bot de Discord al servidor de Discord
discord_client.run(token)
