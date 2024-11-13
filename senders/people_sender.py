from senders import AbstractSender
import random
import json
import numpy as np


class PeopleSender(AbstractSender):
    def __init__(self, framerate: float = 10, new_detection_chance: float = 0.1, remove_detection_chance: float = 0.1, move_speed: float = 0.1):
        super().__init__(framerate)

        self.index = 0
        self.bounding_boxes = [[self.index, 0.5, 0.5, 0.2, 0.4]]
        self.new_detection_chance = new_detection_chance
        self.remove_detection_chance = remove_detection_chance
        self.move_speed = move_speed

    def create_message(self) -> str:
        bb_to_remove = []
        for bounding_box in self.bounding_boxes:
            if random.random() < self.remove_detection_chance:
                bb_to_remove.append(bounding_box)

        for bb in bb_to_remove:
            self.bounding_boxes.remove(bb)

        if random.random() < self.new_detection_chance:
            self.bounding_boxes.append(self.create_detection())

        for bb in self.bounding_boxes:
            self.move_bounding_box(bb)

        message = {
            "event": "people",
            "data": {
                "people": [
                    {
                        "id": index,
                        "bounding_box": {
                            "x": x,
                            "y": y,
                            "width": width,
                            "height": height
                        }
                    }
                    for index, x, y, width, height in self.bounding_boxes
                ]
            }
        }

        return json.dumps(message)

    def create_detection(self) -> list[float]:
        x = random.random()
        y = random.random()

        width = abs(random.random() * (1 - x))
        height = abs(random.random() * (1 - y))

        self.index += 1

        return [self.index, x, y, width, height]

    def move_bounding_box(self, bounding_box: list[float]) -> None:
        for i in range(1,5):
            bounding_box[i] = np.clip(bounding_box[i] + (random.random() * 2 - 1) * self.move_speed, 0, 1)

