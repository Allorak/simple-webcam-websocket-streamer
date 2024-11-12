from senders import AbstractSender
import random
import json


class AllScoresSender(AbstractSender):
    def __init__(self, framerate: float = 3, increase_chance: float = 0.5, critical_chance: float = 0.2, new_round_chance: float = 0.001):
        super().__init__(framerate)

        self.scores = [
            {
              "round_critical": 0,
              "round_total": 0,
              "game_critical": 0,
              "game_total": 0
            }
            for _ in range(4)
        ]

        self.increase_chance = increase_chance
        self.critical_chance = critical_chance
        self.new_round_chance = new_round_chance

    def create_message(self) -> str:
        for scores in self.scores:
            if random.random() <= self.increase_chance:
                scores["round_total"] += 1
                scores["game_total"] += 1

                if random.random() <= self.critical_chance:
                    scores["game_critical"] += 1
                    scores["round_critical"] += 1

            if random.random() <= self.new_round_chance:
                scores["round_critical"] = 0
                scores["round_total"] = 0

        message = {
            "event": "scores",
            "data": {
                f"player_{i}": scores for i,scores in enumerate(self.scores)
            }
        }

        return json.dumps(message)