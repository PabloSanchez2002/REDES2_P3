import os
import sys
import discord
import paho.mqtt.client as mqtt


token = "MTEwMDcxODE2MDI3NTA2Njg5MA.GSkF9C.MY1kNb6gpBPOtmoTTqyeovZ82iS8NTbLH6AwCc"
broker_address = "localhost"
broker_port = 1883
topic = "redes2/2321/02/"

class Bridge:
    def __init__() -> None:
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


def main():
    """Punto de entrada de ejecución
    """
    bot = discord()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
