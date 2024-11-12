from senders import AbstractSender
import random
import json

class PlayerListSender(AbstractSender):
    def __init__(self, framerate: float = 1/60):
        super().__init__(framerate)

        self.player_lists = [
            ['Соколов Алексей', 'Андреев Сергей', 'Андреев Дмитрий', 'Попова Мария'],
            ['Орлова Анна', 'Смирнова Екатерина', 'Андреева София', 'Волков Сергей'],
            ['Морозова Анастасия', 'Морозов Алексей', 'Орлова Елена', 'Тихонов Сергей'],
            ['Федорова Екатерина', 'Михайлова Мария', 'Морозов Алексей', 'Иванова Анастасия']
        ]

    def create_message(self) -> str:
        players = random.choice(self.player_lists)

        message = {
            "event": "players",
            "data":{
                "players": {f'player_{i}': player for i, player in enumerate(players)}
            }
        }

        return json.dumps(message)