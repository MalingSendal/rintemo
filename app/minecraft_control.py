# minecraft_control.py

from minecraft.networking.connection import Connection
from minecraft.networking.packets import ChatPacket, PositionAndLookPacket
import threading

class MinecraftController:
    def __init__(self, host, port, username):
        self.conn = Connection(host, port, username=username)
        self.connected = False
        self._connect()

    def _connect(self):
        def run():
            self.conn.connect()
            self.connected = True
        threading.Thread(target=run, daemon=True).start()

    def say(self, message):
        if self.connected:
            chat = ChatPacket()
            chat.message = message
            self.conn.write_packet(chat)

    def set_position(self, x, y, z, yaw=0, pitch=0):
        if self.connected:
            pos = PositionAndLookPacket()
            pos.x = x
            pos.feet_y = y
            pos.z = z
            pos.yaw = yaw
            pos.pitch = pitch
            pos.on_ground = True
            self.conn.write_packet(pos)