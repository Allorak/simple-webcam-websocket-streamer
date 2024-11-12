import json

from senders import AbstractSender
import random


class PlayerChangeSender(AbstractSender):
    def __init__(self, framerate: float = 1/30):
        super().__init__(framerate)
        self.players_list = ["Имя Фамилия", "Иван Иванов", "Player Player", "Василий Пупкин"]

    def create_message(self) -> str:
        message = {
          "event": "active_player",
          "data": {
            "name": random.choice(self.players_list),
            "score": {
              "round_critical": 0,
              "round_total": 0,
              "game_critical": 0,
              "game_total": 0,
            },
            "magnitudes": [random.random() * 20 for _ in range(50)],
            "pose": {
                'nose': (0.5,0.5),
                'left_eye': (0.5,0.5),
                'right_eye': (0.5,0.5),
                'left_ear': (0.5,0.5),
                'right_ear': (0.5,0.5),
                'left_shoulder': (0.5,0.5),
                'right_shoulder': (0.5,0.5),
                'left_elbow': (0.5,0.5),
                'right_elbow': (0.5,0.5),
                'left_wrist': (0.5,0.5),
                'right_wrist': (0.5,0.5),
                'left_hip': (0.5,0.5),
                'right_hip': (0.5,0.5),
                'left_knee': (0.5,0.5),
                'right_knee': (0.5,0.5),
                'left_ankle': (0.5,0.5),
                'right_ankle': (0.5,0.5),
                'left_big_toe': (0.5,0.5),
                'left_small_toe': (0.5,0.5),
                'left_heel': (0.5,0.5),
                'right_big_toe': (0.5,0.5),
                'right_small_toe': (0.5,0.5),
                'right_heel': (0.5,0.5)
            }
          }
        }

        return json.dumps(message)