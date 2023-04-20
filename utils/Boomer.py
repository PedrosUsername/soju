import json

class Boomer:

    def __init__(self, dict):
        self.word = dict["word"]
        self.image = dict["image"]
        self.audio = dict["audio"]
        self.video = dict["video"]

    def to_string(self):
        return json.dumps(self.__dict__)
