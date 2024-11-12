from collections import deque
import json
import random

from senders import AbstractSender


class GraphSender(AbstractSender):
    def __init__(self, framerate: float = 3, high_value_chance = 0.05, low_amplitude = 10, high_amplitude = 50):
        super().__init__(framerate)

        self.magnitudes = deque(maxlen=50)
        self.high_value_chance = high_value_chance
        self.low_amplitude = low_amplitude
        self.high_amplitude = high_amplitude


    def create_message(self) -> str:
        amplitude = self.low_amplitude if random.random() > self.high_value_chance else self.high_amplitude
        new_value = random.random() * amplitude
        self.magnitudes.append(new_value)
        message = {
            "event": "player_magnitudes",
            "data": {
                "magnitudes": list(self.magnitudes)
            }
        }
        return json.dumps(message)