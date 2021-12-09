import asyncio
import threading
from ast import literal_eval
from configparser import ConfigParser
import websockets
import json


parser = ConfigParser()
parser.read('config.ini')


class Client:

    def __init__(self):
        self.run = False
        self.blue = True
        self.robot = literal_eval(parser.get('robot', 'robot_id'))
        self.host = literal_eval(parser.get('websocket', 'host'))
        self.port = literal_eval(parser.get('websocket', 'port'))

    async def listen(self):
        print("Connecting to " + str(self.host) + " on port " + str(self.port))
        uri = "ws://" + str(self.host) + ":" + str(self.port)
        async with websockets.connect(uri) as ws:
            while True:
                msg = await ws.recv()
                cmd = json.loads(msg)
                print("Received message from server: " + str(cmd))
                try:
                    self.process_command(cmd)
                except ValueError:
                    continue

    def process_command(self, cmd):
        parser.read('config.ini')
        self.robot = literal_eval(parser.get('robot', 'robot_id'))
        if self.robot in cmd["targets"]:
            if cmd["signal"] == "changeID" and self.robot != cmd["robot"]:
                new_robot_id = cmd["robot"]
                try:
                    parser.set('robot', 'robot_id', repr(new_robot_id))
                    with open('../../config.ini', "w") as f:
                        parser.write(f)
                    print(new_robot_id)
                    self.robot = new_robot_id
                except ValueError:
                    print("Invalid robot id.")
            elif cmd["signal"] == "stop":
                self.run = False
            elif cmd["signal"] == "start":
                color = cmd["baskets"][cmd["targets"].index(self.robot)]
                if color == "blue":
                    self.blue = True
                else:
                    self.blue = False
                self.run = True

    def get_current_referee_command(self):
        return self.run, self.blue

    def start_loop(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.listen())
        loop.run_forever()

    def start(self):
        t = threading.Thread(target=self.start_loop)
        t.start()
