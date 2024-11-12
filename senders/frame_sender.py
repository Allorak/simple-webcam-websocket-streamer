import json
from threading import Thread

from senders import AbstractSender
import cv2
import io
import base64
from PIL import Image


class FrameSender(AbstractSender):
    def __init__(self, capture, framerate: float = 15, image_size: tuple[int,int] = (896,504)):
        super().__init__(framerate)

        self.capture = capture
        self.last_frame = []
        self.image_size = image_size

        self.reading_thread = Thread(target=self.read, daemon=True)
        self.reading_thread.start()

    def create_message(self) -> str:
        base64_image = self.convert_image_to_json(self.last_frame)
        message = {
            "event": "player_frame",
            "data":{
                "frame": base64_image,
                "area": {
                  "x": 0.3,
                  "y": 0.3,
                  "width": 0.2,
                  "height": 0.5
                }
            }
        }
        return json.dumps(message)

    def read(self):
        while True:
            ret, frame = self.capture.read()

            if not ret:
                continue

            self.last_frame = frame

    def convert_image_to_json(self, image):
        image = cv2.resize(image, self.image_size)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image.astype("uint8"))
        raw_bytes = io.BytesIO()
        im.save(raw_bytes, "JPEG")
        raw_bytes.seek(0)
        return base64.b64encode(raw_bytes.read()).decode("utf-8")