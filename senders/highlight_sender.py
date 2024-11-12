import random
from datetime import datetime
import json

from senders import AbstractSender


class HighlightSender(AbstractSender):
    def __init__(self, framerate: float = 1/5, camera_amount: int = 16):
        super().__init__(framerate)

        self.camera_amount = camera_amount

    def create_message(self) -> str:
        player = f"player_{random.randint(1,4)}"
        timestamp = datetime.now().strftime("%H:%M:%S")
        has_cameras = random.random() <= 0.5
        cameras = []

        if has_cameras:
            visible_cameras_amount = random.randint(1, self.camera_amount)

            for _ in range(visible_cameras_amount):
                cameras.append(random.randint(1, self.camera_amount))

            cameras.sort()

        message = {
            "event": "highlight",
            "data": {
                "player": player,
                "timestamp": timestamp,
                "cameras": cameras
            }
        }

        return json.dumps(message)