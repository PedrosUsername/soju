import json

class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''

    def __init__(self, dict):
        '''
        Parameters:
          dict (dict) dictionary from JSON, containing:

            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        '''

        self.word = dict["word"]
        self.start = dict["start"]
        self.end = dict["end"]
        self.image = dict["image"]
        self.audio = dict["audio"]

    def to_string(self):
        ''' Returns a string describing this instance '''
        return json.dumps(self.__dict__)
