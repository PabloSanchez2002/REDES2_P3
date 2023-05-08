from discord.ext import commands

from discord import Intents as intent
from threading import Thread, Semaphore

import paho.mqtt.client as mqtt
from multiprocessing import Queue

import time
import signal
import os

import asyncio


SHARED = "redes2/2301/06"
TOKEN = 'MTA5NjQ1NDk1NTgxODMwNzY4NQ.Gsi9Fj.Tr6mqftd7A5hJbk_pni08yk8zuNcbIVtCULeEw'
CHANNEL_ID = 1096457830753640510

connected_devices = []


def mqtt_manager(mp_queue: Queue, sensors_queue: Queue, clock_queue: Queue, bot_pid):
    mqtt_client = mqtt.Client(client_id='Bot')

    def on_connect(client, userdata, flags, rc):
        print(f"[+] Bot connected to mqtt")

        mqtt_client.subscribe(SHARED + f"/bot/#")

    def on_message(client, userdata, message):

        if message.topic == (SHARED + f"/bot/response"):
            mp_queue.put(message.payload.decode())

        elif message.topic == (SHARED + f"/bot/response/ping"):
            connected_devices.append(message.payload.decode())

            mp_queue.put(f"Device {message.payload.decode()} is active")

        elif message.topic == (SHARED + '/bot/response/event_response'):

            os.kill(bot_pid, signal.SIGALRM)
            sensors_queue.put(message.payload.decode())

        elif message.topic == (SHARED + '/bot/response/clock_event'):

            os.kill(bot_pid, signal.SIGUSR1)
            clock_queue.put(message.payload.decode())

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect("mqtt.eclipseprojects.io", 1883,
                        keepalive=60, bind_address="")

    mqtt_client.loop_start()

    while True:
        cmd = mp_queue.get(block=True)

        commands = str(cmd).split(" ")

        match commands[0]:
            case "on":
                mqtt_client.publish(
                    SHARED + f"/home/switch/on", commands[1])
            case "off":
                mqtt_client.publish(
                    SHARED + f"/home/switch/off", commands[1])
            case"add_room":
                print(str(commands[1]))
                mqtt_client.publish(
                    SHARED + f"/home/set/add_room", str(commands[1]))
            case "add":
                mqtt_client.publish(SHARED + f"/home/add",
                                    str(commands[1]).replace("$", " "))
            case "status":
                device_type, id = commands[1].split("$")

                mqtt_client.publish(
                    SHARED + f"/home/{device_type}/get_status", id)

            case "connect":
                device_type, id = commands[1].split("$")
                mqtt_client.publish(
                    SHARED + f"/home/{device_type}/connect", id)

            case "add_rule":
                mqtt_client.publish(
                    SHARED + f"/home/add_rule", commands[1])

            case "remove_rule":
                mqtt_client.publish(
                    SHARED + f"/home/remove_rule", commands[1])

            case "edit_rule":
                mqtt_client.publish(
                    SHARED + f"/home/edit_rule", commands[1])

            case "edit_device":
                mqtt_client.publish(
                    SHARED + f"/home/edit_device", commands[1])


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(intents=intent.all(), command_prefix='!')

        self.message1 = "[INFO]: Bot now online"
        self.message2 = "Bot still online"
        self.add_commands()

        self.mp_queue = Queue()
        self.sensor_queue = Queue()
        self.clock_queue = Queue()

        self.loop = asyncio.get_event_loop()

        signal.signal(signal.SIGALRM, self.event)
        signal.signal(signal.SIGUSR1, self.clock_event)

        Thread(target=mqtt_manager, args=(self.mp_queue, self.sensor_queue,
               self.clock_queue, os.getpid(), ), daemon=True).start()

    async def on_ready(self):
        print(self.message1)

    def clock_event(self, signum, frame):
        temp = self.clock_queue.get(block=True)

        self.loop.create_task(self.send(temp))

    def event(self, signum, frame):
        temp = self.sensor_queue.get(block=True)

        self.loop.create_task(self.send(temp))

    async def send(self, msg):

        await self.get_channel(CHANNEL_ID).send(msg)

    def add_commands(self):
        @self.command(name="connect", pass_context=True)
        async def connect(ctx, device_type, id):
            self.mp_queue.put(f"connect {device_type}${id}")

            response = ""
            try:
                response = self.mp_queue.get(block=True, timeout=4)
            except:
                await self.get_channel(CHANNEL_ID).send(f"Device {id} not online")

                return

            await self.get_channel(CHANNEL_ID).send(response)

        @self.command(name="status", pass_context=True)
        async def status(ctx, device_type, id):
           self.mp_queue.put(f"status {device_type}${id}")
           response = self.mp_queue.get(block=True)

           await self.get_channel(CHANNEL_ID).send(response)

        @self.command(name='add', pass_context=True)
        async def connect_switch(ctx, device_type=None,  id=None, host="mqtt.eclipseprojects.io", port=1883, prob=0.3):

            if not id and not device_type:
                await self.get_channel(CHANNEL_ID).send('se debe indicar el id del dispositvo y el espacion en donde se ubica')
            else:
                self.mp_queue.put(
                    f"add {device_type}${id}${host}${port}${prob}")
                respone = self.mp_queue.get(block=True)

                await self.get_channel(CHANNEL_ID).send(respone)

        @self.command(name='on', pass_context=True)
        async def up_switch(ctx, device_type=None, id=None):

            if not id and not device_type:
                await self.get_channel(CHANNEL_ID).send('Se debe indicar el id y el tipo de dispositvo')
            elif device_type != "switch":
                await self.get_channel(CHANNEL_ID).send('Solo los switchs pueden hacer up y down')
            else:
                self.mp_queue.put(f"on {id}")
                response = self.mp_queue.get(block=True)
                await self.get_channel(CHANNEL_ID).send(response)

        @self.command(name='off', pass_context=True)
        async def down_switch(ctx, device_type=None, id=None):

            if not id and not device_type:
                await self.get_channel(CHANNEL_ID).send('Se debe indicar el id y el tipo de dispositvo')
            elif device_type != "switch":
                await self.get_channel(CHANNEL_ID).send('Solo los switchs pueden hacer on y off')
            else:
                self.mp_queue.put(f"off {id}")
                response = self.mp_queue.get(block=True)
                await self.get_channel(CHANNEL_ID).send(response)

        @self.command(name='add_rule', pass_context=True)
        async def add_rule(ctx, device_type=None, device_id=None, cond=None, value=None, then_state=None, action_device=None, action=None):

            if device_type is None or device_id is None or cond is None or value is None or then_state is None or action_device is None or action is None:
                await self.get_channel(CHANNEL_ID).send("Error, para editar una regla debes introducir: !add_rule <switch o clock> <id de dispositivo> <'>' o '<' o '='> <hora o temperatura> then <id del switch afectado> <on o off>")
            payload = f"{device_type}${device_id}${cond}${value}${then_state}${action_device}${action}"
            self.mp_queue.put(f"add_rule {payload}")
            response = self.mp_queue.get(block=True)
            await self.get_channel(CHANNEL_ID).send(response)

        @self.command(name='remove_rule', pass_context=True)
        async def remove_rule(ctx, id=None):

            if id is None:
                await self.get_channel(CHANNEL_ID).send("Error, para borrar una regla debes introducir: !remove_rule <id de regla>")
            self.mp_queue.put(f"remove_rule {id}")
            response = self.mp_queue.get(block=True)
            await self.get_channel(CHANNEL_ID).send(response)

        @self.command(name='edit_rule', pass_context=True)
        async def edit_rule(ctx, id=None, device_type=None, device_id=None, cond=None, value=None, then_state=None, action_device=None, action=None):

            if id is None or device_type is None or device_id is None or cond is None or value is None or then_state is None or action_device is None or action is None:
                await self.get_channel(CHANNEL_ID).send("Para editar una regla debes introducir: !edit_rule <id de regla> <switch o clock> <id de dispositivo> <'>' o '<' o '='> <hora o temperatura> then <id del switch afectado> <on o off>")

            payload = f"{id}#{device_type}${device_id}${cond}${value}${then_state}${action_device}${action}"

            self.mp_queue.put(f"edit_rule {payload}")
            response = self.mp_queue.get(block=True)

            await self.get_channel(CHANNEL_ID).send(response)

        @self.command(name='remove_device', pass_context=True)
        async def remove_device(ctx, id=None, host=None, port=None, prob=None):

            if id is None or host is None or port is None or prob is None:
                await self.get_channel(CHANNEL_ID).send("Para editar un dispositivo se debe indicar: !edit_device <id> <host> <port> <prob>")

            payload = f"{id}${host}${port}${prob}"
            self.mp_queue.put(f"edit_device {payload}")
            response = self.mp_queue.get(block=True)

            await self.get_channel(CHANNEL_ID).send(response)


if __name__ == '__main__':
    bot = Bot()
    bot.run(TOKEN)
