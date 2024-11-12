from abc import abstractmethod, ABC
import time

from fastapi import WebSocket
import asyncio


class AbstractSender(ABC):
    def __init__(self, framerate: float = 15):
        self.delay = 1 / framerate
        self.last_send_time = 0
        self.connections: list[WebSocket] = []

    async def start(self):
        while True:
            await self.send()

    async def send(self):
        if time.time() - self.last_send_time < self.delay:
            return

        self.last_send_time = time.time()

        for connection in self.connections:
            await connection.send_json(self.create_message())

        await asyncio.sleep(0.01)

    @abstractmethod
    def create_message(self) -> str:
        pass

    async def add_connection(self, websocket: WebSocket):
        self.connections.append(websocket)

    async def remove_connection(self, websocket: WebSocket):
        self.connections.remove(websocket)