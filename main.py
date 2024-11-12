import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json
from loguru import logger
from contextlib import asynccontextmanager
import cv2
from senders import AbstractSender, FrameSender, PoseSender, PlayerScoreSender

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

if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    senders_list.append(FrameSender(capture))
    senders_list.append(PoseSender(framerate=5))
    senders_list.append(PlayerScoreSender(framerate=0.3))

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


    host = '127.0.0.1'
    port = 15555
    api = FastAPI(lifespan=lifespan)
    api.add_websocket_route("/ws", process)

    uvicorn.run(api, host=host, port=port)

