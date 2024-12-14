from enum import Enum


class Symbols(Enum):
    SPADES = ("♠️", 12.5)
    CLUBS = ("♣️", 12.5)
    HEARTS = ("♥️", 12.5)
    DIAMONDS = ("♦️", 12.5)
    CLOVERS = ("🍀", 10.5)
    EYES = ("🧿", 10.0)
    CROWN = ("👑", 8.5)
    MAGIC = ("🔮", 8.5)
    GOLD = ("⚜️", 7.0)
    WILD = ("🎰", 53.4)
    BONUS = ("💎", 20.1)

    def __init__(self, emoji, probability):
        self.__emoji = str(emoji)
        #if probability <= 0:
            #raise ValueError(f"Probability для {emoji} должна быть больше 0.")
        self.__probability = float(probability)

    @property
    def emoji(self):
        return self.__emoji

    @property
    def probability(self):
        return self.__probability

    @classmethod
    def total_probability(cls):
        return sum(symbol.probability for symbol in cls)
