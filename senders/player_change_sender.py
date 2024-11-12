import json

from senders import AbstractSender
import time
import random
import asyncio


class PlayerChangeSender(AbstractSender):
    def __init__(self, framerate: float = 15, player_change_chance: float = 0.001):
        super().__init__(framerate)
        self.player_change_chance = player_change_chance
        self.players_list = ["Имя Фамилия", "Иван Иванов", "Player Player", "Василий Пупкин"]

    async def send(self):
        if time.time() - self.last_send_time < self.delay:
            return

        self.last_send_time = time.time()

        if random.random() <= self.player_change_chance:
            for connection in self.connections:
                await connection.send_json(self.create_message())

        await asyncio.sleep(0.01)

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