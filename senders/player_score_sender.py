import random
import json

from senders import AbstractSender


class PlayerScoreSender(AbstractSender):
    def __init__(self, framerate: float = 2, critical_chance: float = 0.5, new_round_chance: float = 0.05):
        super().__init__(framerate)

        self.round_critical = 0
        self.round_total = 0
        self.game_critical = 0
        self.game_total = 0

        self.critical_chance = critical_chance
        self.new_round_chance = new_round_chance

    def create_message(self) -> str:
        self.round_total += 1
        self.game_total += 1

        if random.random() <= self.critical_chance:
            self.game_critical += 1
            self.round_critical += 1

        if random.random() <= self.new_round_chance:
            self.round_critical = 0
            self.round_total = 0

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
