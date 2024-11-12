import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json
from loguru import logger
from contextlib import asynccontextmanager
import cv2
from senders import AbstractSender, FrameSender, PeopleSender

senders_list: list[AbstractSender] = []

async def process(websocket: WebSocket):
    await websocket.accept()

    global senders_list

    for sender in senders_list:
        await sender.add_connection(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            logger.info(message)
    except WebSocketDisconnect as e:
        for sender in senders_list:
            await sender.remove_connection(websocket)

@asynccontextmanager
async def lifespan(app: FastAPI):
    tasks = [asyncio.create_task(sender.start()) for sender in senders_list]

    yield

    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    source = 0
    capture = cv2.VideoCapture(source)

    senders_list.append(FrameSender(capture))
    senders_list.append(PeopleSender())

    host = '127.0.0.1'
    port = 15555
    api = FastAPI(lifespan=lifespan)
    api.add_websocket_route("/ws", process)

    uvicorn.run(api, host=host, port=port)

