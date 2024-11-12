import random
import json

from senders import AbstractSender


class PoseSender(AbstractSender):
    def __init__(self, framerate: float = 3):
        super().__init__(framerate)

    def create_message(self) -> str:
        keypoints = {
            'nose': self.random_keypoint((0.4, 0.4)),
            'left_eye': self.random_keypoint((0.41, 0.38)),
            'right_eye': self.random_keypoint( (0.39, 0.38)),
            'left_ear': self.random_keypoint((0.43, 0.4)),
            'right_ear':  self.random_keypoint((0.37, 0.4)),
            'left_shoulder':  self.random_keypoint((0.45, 0.45)),
            'right_shoulder': self.random_keypoint((0.35, 0.45)),
            'left_elbow': self.random_keypoint((0.46, 0.5)),
            'right_elbow': self.random_keypoint((0.34, 0.5)),
            'left_wrist': self.random_keypoint((0.47, 0.55)),
            'right_wrist': self.random_keypoint((0.33, 0.55)),
            'left_hip': self.random_keypoint((0.43, 0.56)),
            'right_hip': self.random_keypoint((0.37, 0.56)),
            'left_knee': self.random_keypoint((0.44, 0.6)),
            'right_knee': self.random_keypoint((0.36, 0.6)),
            'left_ankle': self.random_keypoint((0.43, 0.66)),
            'right_ankle': self.random_keypoint((0.37, 0.66)),
            'left_big_toe': self.random_keypoint((0.45, 0.73)),
            'left_small_toe': self.random_keypoint((0.46, 0.71)),
            'left_heel': self.random_keypoint((0.43, 0.7)),
            'right_big_toe': self.random_keypoint((0.35, 0.73)),
            'right_small_toe': self.random_keypoint((0.34, 0.71)),
            'right_heel': self.random_keypoint((0.37, 0.7)),
        }
        message = {
            "event": "pose",
            "data": {
                "pose": keypoints
            }
        }
        return json.dumps(message)

    def random_keypoint(self, center: tuple[float, float], radius: float = 0.015):
        x,y = center

        x_variance = (random.random() * 2 - 1) * radius
        y_variance = (random.random() * 2 - 1) * radius

        return {"x": x + x_variance, "y": y + y_variance}
