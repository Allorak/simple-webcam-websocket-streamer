import random
import time
import asyncio
import json

from senders import AbstractSender


class PlayerScoreSender(AbstractSender):
    def __init__(self, framerate: float = 15, increase_chance: float = 0.2, critical_chance: float = 0.5, new_round_chance: float = 0.05):
        super().__init__(framerate)

        self.round_critical = 0
        self.round_total = 0
        self.game_critical = 0
        self.game_total = 0

        self.increase_chance = increase_chance
        self.critical_chance = critical_chance
        self.new_round_chance = new_round_chance

    async def send(self):
        if time.time() - self.last_send_time < self.delay:
            return

        self.last_send_time = time.time()

        if random.random() <= self.increase_chance:
            self.round_total += 1
            self.game_total += 1

            if random.random() <= self.critical_chance:
                self.game_critical += 1
                self.round_critical += 1

            if random.random() <= self.new_round_chance:
                self.round_critical = 0
                self.round_total = 0

            for connection in self.connections:
                await connection.send_json(self.create_message())

        await asyncio.sleep(0.01)

    def create_message(self) -> str:
        message = {
            "event": "player_score",
            "data": {
                "score": {
                    "round_critical": self.round_critical,
                    "round_total": self.round_total,
                    "game_critical": self.game_critical,
                    "game_total": self.game_total
                }
            }
        }

        return json.dumps(message)
