import os
import sys
import discord
import paho.mqtt.client as mqtt
import argparse as ag


token = "MTEwMDcxODE2MDI3NTA2Njg5MA.GSkF9C.MY1kNb6gpBPOtmoTTqyeovZ82iS8NTbLH6AwCc"
broker_address = "localhost"
broker_port = 1883
topic = "redes2/2321/02/"


class Bridge:
    def __init__(self) -> None:

        self.client = mqtt.Client()
        self.client.connect(broker_address, broker_port)
        self.client.subscribe(topic+"bridge_receive")
        self.send_topic = topic+"bridge_send"
        self.client.on_message = self.on_rule_message

        intents = discord.Intents.all()
        intents.members = True

        discord_client = discord.Client(intents=intents)

        @discord_client.event
        async def on_ready():
            print('Bot de Discord conectado como {0.user}'.format(
                discord_client))

        @discord_client.event
        async def on_message(message):
            if message.author == discord_client.user:
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
                        # create_sensor(int(tokens[2]))
                    elif tokens[1] == "actuador":
                        self.client.publish(
                            self.send_topic, "bridge:newactuador:" + tokens[2])
                        # create_actuador(int(tokens[2]))

                    elif tokens[1] == "regla":
                        self.client.publish(
                            self.send_topic, "bridge:newrule:" + str(tokens[2]) + ":" + str(tokens[3]) + ":" + str(tokens[3]) + ":" + str(tokens[3]) + ":" + str(tokens[6]))
                        # create_regla(tokens[2], tokens[3], tokens[4], tokens[5], tokens[6])

                elif tokens[0] == "obtener":
                    print("entra en obtener:" + self.send_topic)
                    # mensaje = valores[tokens[1]]
                    # await message.channel.send(mensaje.format(message))
                    self.client.publish(
                        self.send_topic, "bridge:get:" + str(tokens[1]))

                else:
                    print("El comando que has introducido no es valido.")

                # except:
                #    print("El comando que has introducido no funcionó.")
        try:
            discord_client.run(token)
        except:
            return

    async def on_rule_message(self, client, userdata, msg):
        print("he recibido:" + msg)
        #await message.channel.send(message.format(message))


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
