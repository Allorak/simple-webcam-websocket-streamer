from abc import abstractmethod, ABC
import time

from fastapi import WebSocket
import asyncio


class AbstractSender(ABC):
    def __init__(self, framerate: float = 15):
        self.delay = 1 / framerate
        self.connections: list[WebSocket] = []

    async def start(self):
        while True:
            await self.send()
            await asyncio.sleep(self.delay)

    async def send(self):
        for connection in self.connections:
            await connection.send_json(self.create_message())

    @abstractmethod
    def create_message(self) -> str:
        pass

    async def add_connection(self, websocket: WebSocket):
        self.connections.append(websocket)

    async def remove_connection(self, websocket: WebSocket):
        self.connections.remove(websocket)