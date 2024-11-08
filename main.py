import time
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from loguru import logger
import json
from PIL import Image
import io
import base64
import asyncio
from threading import Thread
import uvicorn

image_size = (896,504)
framerate = 15
host = '127.0.0.1'
port = 15555

last_send_time = 0
connections: list[WebSocket] = []

async def process(websocket: WebSocket):
    await websocket.accept()

    global connections
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            logger.info(message)
    except WebSocketDisconnect as e:
        connections.remove(websocket)

def convert_image_to_json(image):
    global image_size
    image = cv2.resize(image, image_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(image.astype("uint8"))
    raw_bytes = io.BytesIO()
    im.save(raw_bytes, "JPEG")
    raw_bytes.seek(0)
    return base64.b64encode(raw_bytes.read()).decode("utf-8")


async def send_frame(frame: np.ndarray):
    message = convert_image_to_json(frame)

    global last_send_time, framerate

    if time.time() - last_send_time < 1/framerate:
        return

    last_send_time = time.time()

    global connections
    for connection in connections:
        await connection.send_json(message)

def start(app):
    global host, port
    Thread(target=uvicorn.run, kwargs={"app": app, "host": host, "port": port}, daemon=True).start()

async def send_capture(capture):
    while True:
        ret, frame = capture.read()

        if not ret:
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        await send_frame(frame)

if __name__ == "__main__":
    source = 0
    capture = cv2.VideoCapture(source)
    api = FastAPI()
    api.add_websocket_route("/ws", process)
    start(api)

    asyncio.get_event_loop().run_until_complete(send_capture(capture))

